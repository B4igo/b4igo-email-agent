"""Thin wrappers around the Docker SDK for the admin panel.

All functions assume `/var/run/docker.sock` is mounted into this container.
The set of containers the panel manages is restricted to `config.PANEL_CONTAINERS`
to keep the blast radius bounded — even if someone slips through the auth gate
they can't shell into arbitrary containers on the host.
"""

from __future__ import annotations

import asyncio
from typing import AsyncIterator, Optional

import docker
from docker.errors import APIError, NotFound
from docker.models.containers import Container

from config import PANEL_CONTAINERS, SELF_CONTAINER_NAME

_client: Optional[docker.DockerClient] = None


def client() -> docker.DockerClient:
    global _client
    if _client is None:
        _client = docker.from_env()
    return _client


def is_managed(name: str) -> bool:
    if name == SELF_CONTAINER_NAME:
        return False
    return name in PANEL_CONTAINERS


def get(name: str) -> Container:
    if not is_managed(name):
        raise PermissionError(f"Container '{name}' is not managed by this panel")
    return client().containers.get(name)


def safe_get(name: str) -> Optional[Container]:
    try:
        return get(name)
    except (NotFound, PermissionError):
        return None


def list_summaries() -> list[dict]:
    """Snapshot of every managed container's state for the dashboard."""
    out = []
    for name in PANEL_CONTAINERS:
        c = safe_get(name)
        if c is None:
            out.append({
                "name": name,
                "state": "absent",
                "status": "not found",
                "image": "",
                "ports": {},
                "health": None,
                "started_at": None,
            })
            continue
        attrs = c.attrs
        state = attrs.get("State", {})
        out.append({
            "name": name,
            "state": state.get("Status", "unknown"),
            "status": c.status,
            "image": (attrs.get("Config", {}).get("Image", "") or ""),
            "ports": attrs.get("NetworkSettings", {}).get("Ports", {}) or {},
            "health": (state.get("Health") or {}).get("Status"),
            "started_at": state.get("StartedAt"),
        })
    return out


def inspect(name: str) -> dict:
    c = get(name)
    a = c.attrs
    cfg = a.get("Config", {}) or {}
    state = a.get("State", {}) or {}
    return {
        "name": name,
        "image": cfg.get("Image", ""),
        "cmd": cfg.get("Cmd") or cfg.get("Entrypoint") or [],
        "env": cfg.get("Env") or [],
        "ports": (a.get("NetworkSettings", {}) or {}).get("Ports", {}) or {},
        "networks": list(((a.get("NetworkSettings", {}) or {}).get("Networks", {}) or {}).keys()),
        "state": state.get("Status"),
        "health": (state.get("Health") or {}).get("Status"),
        "started_at": state.get("StartedAt"),
        "restart_count": a.get("RestartCount", 0),
    }


def lifecycle(name: str, action: str) -> str:
    c = get(name)
    if action == "start":
        c.start()
    elif action == "stop":
        c.stop(timeout=10)
    elif action == "restart":
        c.restart(timeout=10)
    elif action == "kill":
        c.kill()
    else:
        raise ValueError(f"Unknown lifecycle action: {action}")
    c.reload()
    return c.status


def tail_logs(name: str, lines: int = 200) -> str:
    c = get(name)
    try:
        return c.logs(tail=lines, timestamps=False).decode("utf-8", errors="replace")
    except APIError as e:
        return f"<error reading logs: {e}>"


async def stream_logs(name: str, since: Optional[int] = None) -> AsyncIterator[str]:
    """Yield log lines as they appear. Runs blocking docker stream in a thread."""
    c = get(name)
    loop = asyncio.get_event_loop()
    queue: asyncio.Queue[Optional[str]] = asyncio.Queue(maxsize=1024)

    def _pump():
        try:
            stream = c.logs(stream=True, follow=True, since=since, tail=200)
            buf = b""
            for chunk in stream:
                buf += chunk
                while b"\n" in buf:
                    line, buf = buf.split(b"\n", 1)
                    asyncio.run_coroutine_threadsafe(
                        queue.put(line.decode("utf-8", errors="replace")), loop,
                    )
            if buf:
                asyncio.run_coroutine_threadsafe(
                    queue.put(buf.decode("utf-8", errors="replace")), loop,
                )
        except Exception as e:
            asyncio.run_coroutine_threadsafe(queue.put(f"<stream error: {e}>"), loop)
        finally:
            asyncio.run_coroutine_threadsafe(queue.put(None), loop)

    task = loop.run_in_executor(None, _pump)
    try:
        while True:
            line = await queue.get()
            if line is None:
                break
            yield line
    finally:
        task.cancel()


def exec_create(name: str, cmd: list[str]) -> str:
    c = get(name)
    api = client().api
    resp = api.exec_create(
        c.id,
        cmd,
        stdin=True,
        stdout=True,
        stderr=True,
        tty=True,
    )
    return resp["Id"]


def exec_start_socket(exec_id: str):
    """Open a raw, bidirectional socket against an exec instance."""
    api = client().api
    sock = api.exec_start(exec_id, detach=False, tty=True, stream=False, socket=True)
    if hasattr(sock, "_sock"):
        sock._sock.setblocking(False)
        return sock._sock
    sock.setblocking(False)
    return sock


def exec_resize(exec_id: str, rows: int, cols: int) -> None:
    try:
        client().api.exec_resize(exec_id, height=rows, width=cols)
    except APIError:
        pass


def get_last_log_line(name: str) -> str:
    c = safe_get(name)
    if c is None:
        return ""
    try:
        raw = c.logs(tail=1).decode("utf-8", errors="replace").strip()
        return raw.splitlines()[-1] if raw else ""
    except APIError:
        return ""
