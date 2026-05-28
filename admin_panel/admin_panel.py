"""B4iGO admin panel - FastAPI service.

Single-file FastAPI app exposing the routes described in templates/. Anything
non-trivial lives in `docker_ops.py` (Docker socket interactions) or
`demo_actions.py` (SMTP / queue / reset).
"""

from __future__ import annotations

import asyncio
import json
import logging
import time
from dataclasses import asdict
from pathlib import Path

import config
import demo_actions
import docker_ops
import e2e_runner
from fastapi import (
    Depends,
    FastAPI,
    Form,
    HTTPException,
    Request,
    WebSocket,
    WebSocketDisconnect,
)
from fastapi.responses import (
    HTMLResponse,
    JSONResponse,
    PlainTextResponse,
    RedirectResponse,
    StreamingResponse,
)
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from itsdangerous import BadSignature, TimestampSigner

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger("admin-panel")

app = FastAPI(title="B4iGO Admin Panel")
app.mount(
    "/static",
    StaticFiles(directory=str(Path(__file__).parent / "static")),
    name="static",
)
templates = Jinja2Templates(directory=str(Path(__file__).parent / "templates"))

signer = TimestampSigner(config.SESSION_SECRET)


# ---------- Auth ----------


def _is_authenticated(request: Request) -> bool:
    token = request.cookies.get(config.SESSION_COOKIE)
    if not token:
        return False
    try:
        signer.unsign(token, max_age=config.SESSION_TTL_SECONDS)
        return True
    except BadSignature:
        return False


def require_auth(request: Request):
    """Reject unauthenticated requests with HTTP 401."""
    if not _is_authenticated(request):
        raise HTTPException(status_code=401, detail="Not authenticated")


@app.middleware("http")
async def auth_middleware(request: Request, call_next):
    """Redirect unauthenticated users to the login page."""
    path = request.url.path
    if (
        path.startswith("/static")
        or path in ("/login", "/healthz")
        or _is_authenticated(request)
    ):
        return await call_next(request)
    return RedirectResponse(url=f"/login?next={path}", status_code=302)


@app.get("/login", response_class=HTMLResponse)
async def login_form(request: Request, next: str = "/", error: str | None = None):
    """Render the login form."""
    return templates.TemplateResponse(
        request,
        "login.html",
        {"next": next, "error": error},
    )


@app.post("/login")
async def login_submit(
    request: Request,
    password: str = Form(...),
    next: str = Form("/"),
):
    """Validate the password and start a signed session."""
    if password != config.ADMIN_PASSWORD:
        return RedirectResponse(
            url=f"/login?next={next}&error=Invalid+password",
            status_code=303,
        )
    token = signer.sign(b"ok").decode()
    response = RedirectResponse(url=next or "/", status_code=303)
    response.set_cookie(
        config.SESSION_COOKIE,
        token,
        max_age=config.SESSION_TTL_SECONDS,
        httponly=True,
        samesite="lax",
    )
    return response


@app.post("/logout")
async def logout():
    """Clear the session cookie and bounce to login."""
    response = RedirectResponse(url="/login", status_code=303)
    response.delete_cookie(config.SESSION_COOKIE)
    return response


@app.get("/healthz")
async def healthz():
    """Report basic liveness for the admin panel."""
    return {"ok": True}


# ---------- Dashboard ----------


@app.get("/", response_class=HTMLResponse)
async def dashboard(request: Request):
    """Render the container overview dashboard."""
    summaries = docker_ops.list_summaries()
    return templates.TemplateResponse(
        request,
        "dashboard.html",
        {"summaries": summaries, "active": "dashboard"},
    )


@app.get("/health-data")
async def health_data(_: None = Depends(require_auth)):
    """Return container summaries as JSON for the dashboard auto-refresh."""
    rows = docker_ops.list_summaries()
    for row in rows:
        row["last_log"] = docker_ops.get_last_log_line(row["name"])
    return JSONResponse(rows)


# ---------- Containers ----------


@app.get("/containers/{name}", response_class=HTMLResponse)
async def container_view(request: Request, name: str):
    """Render the per-container detail page with logs and actions."""
    if not docker_ops.is_managed(name):
        raise HTTPException(404, f"Container '{name}' is not managed")
    info = docker_ops.inspect(name)
    log_tail = docker_ops.tail_logs(name, lines=200)
    return templates.TemplateResponse(
        request,
        "container.html",
        {
            "info": info,
            "log_tail": log_tail,
            "containers": config.PANEL_CONTAINERS,
            "active": "containers",
        },
    )


@app.post("/containers/{name}/lifecycle")
async def container_lifecycle(name: str, action: str = Form(...)):
    """Start, stop, restart, or kill one managed container."""
    if action not in {"start", "stop", "restart", "kill"}:
        raise HTTPException(400, "Invalid action")
    try:
        new_state = docker_ops.lifecycle(name, action)
    except PermissionError as e:
        raise HTTPException(403, str(e)) from e
    return PlainTextResponse(f"OK: {action} -> {new_state}")


@app.get("/containers/{name}/logs/stream")
async def container_logs_stream(name: str):
    """Stream live container logs as server-sent events."""
    if not docker_ops.is_managed(name):
        raise HTTPException(404)

    async def gen():
        try:
            since = int(time.time())
            async for line in docker_ops.stream_logs(name, since=since):
                yield f"data: {json.dumps({'line': line})}\n\n"
        except asyncio.CancelledError:
            return

    return StreamingResponse(gen(), media_type="text/event-stream")


# ---------- Terminal WebSocket ----------


@app.websocket("/containers/{name}/exec")
async def container_exec(websocket: WebSocket, name: str):
    """Open a websocket-backed shell inside the named container."""
    if not _is_authenticated(websocket):
        await websocket.close(code=1008)
        return
    if not docker_ops.is_managed(name):
        await websocket.close(code=1008)
        return

    await websocket.accept()

    shells = [["/bin/bash"], ["/bin/sh"]]
    exec_id: str | None = None
    sock = None
    last_err: Exception | None = None
    for sh in shells:
        try:
            exec_id = docker_ops.exec_create(name, sh)
            sock = docker_ops.exec_start_socket(exec_id)
            break
        except Exception as e:
            last_err = e
            continue
    if sock is None or exec_id is None:
        await websocket.send_text(f"\r\n[exec failed: {last_err}]\r\n")
        await websocket.close()
        return

    loop = asyncio.get_event_loop()
    closed = asyncio.Event()

    async def from_container():
        while not closed.is_set():
            try:
                data = await loop.sock_recv(sock, 4096)
            except (BlockingIOError, OSError):
                await asyncio.sleep(0.05)
                continue
            if not data:
                closed.set()
                break
            try:
                await websocket.send_bytes(data)
            except Exception:
                closed.set()
                break

    async def from_client():
        while not closed.is_set():
            try:
                msg = await websocket.receive()
            except WebSocketDisconnect:
                closed.set()
                return
            if msg["type"] == "websocket.disconnect":
                closed.set()
                return
            if "text" in msg and msg["text"]:
                try:
                    payload = json.loads(msg["text"])
                except ValueError:
                    continue
                if payload.get("type") == "resize":
                    docker_ops.exec_resize(
                        exec_id,
                        int(payload.get("rows", 24)),
                        int(payload.get("cols", 80)),
                    )
                elif payload.get("type") == "input":
                    try:
                        await loop.sock_sendall(sock, payload["data"].encode("utf-8"))
                    except OSError:
                        closed.set()
                        return
            elif "bytes" in msg and msg["bytes"]:
                try:
                    await loop.sock_sendall(sock, msg["bytes"])
                except OSError:
                    closed.set()
                    return

    try:
        await asyncio.gather(from_container(), from_client())
    finally:
        try:
            sock.close()
        except Exception:
            pass


# ---------- Demo actions ----------


@app.get("/demo", response_class=HTMLResponse)
async def demo_page(request: Request):
    """Render the demo actions page."""
    return templates.TemplateResponse(
        request,
        "demo.html",
        {
            "scenarios": demo_actions.SCENARIOS,
            "accounts": demo_actions.SEED_ACCOUNTS,
            "active": "demo",
        },
    )


def _flash(ok: bool, msg: str) -> HTMLResponse:
    cls = "ok" if ok else "err"
    return HTMLResponse(f'<div class="flash {cls}">{msg}</div>')


@app.post("/demo/clear-queue")
async def demo_clear_queue(username: str | None = Form(None)):
    """Clear the backend confirmation queue, optionally scoped to one user."""
    ok, msg = demo_actions.clear_queue(username or None)
    return _flash(ok, msg)


@app.post("/demo/send-scenario")
async def demo_send_scenario(
    scenario_key: str = Form(...),
    recipient: str = Form(...),
):
    """Send one preset scenario email to the chosen recipient."""
    ok, msg = demo_actions.send_scenario(scenario_key, recipient)
    return _flash(ok, msg)


@app.post("/demo/send-bulk")
async def demo_send_bulk(
    count: int = Form(...),
    recipient: str = Form(...),
):
    """Send N scenario emails in a row to the chosen recipient."""
    ok, msg = demo_actions.send_bulk(count, recipient)
    return _flash(ok, msg)


@app.post("/demo/send-custom")
async def demo_send_custom(
    sender: str = Form(...),
    recipient: str = Form(...),
    subject: str = Form(...),
    body: str = Form(...),
):
    """Send one custom email built from the form inputs."""
    ok, msg = demo_actions.send_custom(sender, recipient, subject, body)
    return _flash(ok, msg)


@app.post("/demo/reset")
async def demo_reset():
    """Drain in-flight pipeline state for a fresh demo run."""
    ok, log = demo_actions.one_click_reset()
    items = "".join(f"<li>{line}</li>" for line in log)
    cls = "ok" if ok else "err"
    return HTMLResponse(
        f'<div class="flash {cls}"><strong>Reset complete</strong>'
        f"<ul>{items}</ul></div>"
    )


# ---------- Pipeline trace ----------


@app.get("/trace", response_class=HTMLResponse)
async def trace_page(request: Request):
    """Render the merged pipeline log trace page."""
    return templates.TemplateResponse(
        request,
        "trace.html",
        {
            "stages": list(config.PIPELINE_STAGE_CONTAINERS.items()),
            "active": "trace",
        },
    )


@app.get("/trace/stream")
async def trace_stream():
    """Stream merged log lines from each pipeline-stage container."""
    stages = config.PIPELINE_STAGE_CONTAINERS

    async def gen():
        queue: asyncio.Queue[tuple[str, str]] = asyncio.Queue(maxsize=2048)
        tasks = []

        async def pump_one(stage: str, container: str):
            if not docker_ops.is_managed(container):
                await queue.put((stage, f"<container '{container}' not managed>"))
                return
            try:
                async for line in docker_ops.stream_logs(container):
                    await queue.put((stage, line))
            except Exception as e:
                await queue.put((stage, f"<error: {e}>"))

        for stage, container in stages.items():
            tasks.append(asyncio.create_task(pump_one(stage, container)))

        try:
            while True:
                stage, line = await asyncio.wait_for(queue.get(), timeout=30)
                yield f"data: {json.dumps({'stage': stage, 'line': line})}\n\n"
        except asyncio.TimeoutError:
            yield ": keepalive\n\n"
        except asyncio.CancelledError:
            return
        finally:
            for t in tasks:
                t.cancel()

    return StreamingResponse(gen(), media_type="text/event-stream")


# ---------- AI playground ----------


@app.get("/playground", response_class=HTMLResponse)
async def playground_page(request: Request):
    """Render the AI playground page."""
    return templates.TemplateResponse(
        request,
        "playground.html",
        {
            "ai_url": config.AI_SERVICE_URL,
            "active": "playground",
        },
    )


@app.post("/playground/run")
async def playground_run(text: str = Form(...)):
    """Run text through the AI service in dry-run mode and show the result."""
    ok, result = demo_actions.ai_dry_run(text)
    if not ok:
        return _flash(False, str(result))
    pretty = json.dumps(result, indent=2)
    return HTMLResponse(f'<pre class="json">{pretty}</pre>')


# ---------- E2E pipeline test ----------


@app.get("/e2e", response_class=HTMLResponse)
async def e2e_page(request: Request):
    """Render the end-to-end pipeline test page."""
    return templates.TemplateResponse(
        request,
        "e2e.html",
        {
            "stages": e2e_runner.stages_for_template(),
            "recipient": f"alice@{config.MAIL_DOMAIN}",
            "active": "e2e",
        },
    )


@app.post("/e2e/start")
async def e2e_start(recipient: str = Form(...)):
    """Kick off an end-to-end pipeline test and return the run id."""
    run = await e2e_runner.start_run(
        mail_host=config.MAIL_HOST,
        mail_port=config.MAIL_SMTP_PORT,
        recipient=recipient,
    )
    return JSONResponse({"run_id": run.run_id})


@app.get("/e2e/runs/{run_id}/stream")
async def e2e_stream(run_id: str):
    """Stream stage events for one E2E run as server-sent events."""
    run = e2e_runner.get_run(run_id)
    if run is None:
        raise HTTPException(404, f"Unknown run id {run_id}")

    async def gen():
        try:
            async for evt in e2e_runner.stream_events(run):
                yield f"data: {json.dumps(asdict(evt))}\n\n"
            yield "event: done\ndata: {}\n\n"
        except asyncio.CancelledError:
            return

    return StreamingResponse(gen(), media_type="text/event-stream")
