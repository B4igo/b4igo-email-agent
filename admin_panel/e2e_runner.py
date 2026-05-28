"""End-to-end pipeline test runner for the admin panel.

Drops a synthetic email into the demo mail server and watches the live log
streams of each pipeline stage to confirm the email reaches every component.
The set of stages mirrors the production architecture: mailserver intake,
account-manager IMAP pull (observed via scheduler since account-manager only
emits werkzeug access lines), scheduler queue/handoff, ai-service parse,
backend confirmation enqueue.

Only one run is active at a time. Starting a new run cancels the previous one.
"""

from __future__ import annotations

import asyncio
import logging
import re
import smtplib
import time
import uuid
from dataclasses import dataclass, field
from email.mime.text import MIMEText
from typing import AsyncIterator, Optional

import docker_ops

logger = logging.getLogger("e2e-runner")

RUN_TIMEOUT_SECONDS = 120


@dataclass
class Stage:
    """One observable step in the pipeline."""

    key: str
    label: str
    container: Optional[str]  # None means the admin panel emits the event itself
    pattern: Optional[re.Pattern[str]]
    # Optional secondary pattern that, when matched, marks the stage with the
    # `skipped` state instead of `done`. Used for legitimate non-failure paths
    # (e.g. the AI pipeline classified the email into a domain we do not parse).
    skip_pattern: Optional[re.Pattern[str]] = None


STAGES: list[Stage] = [
    Stage(
        key="smtp_submit",
        label="SMTP submitted",
        container=None,
        pattern=None,
    ),
    Stage(
        key="mail_delivered",
        label="Mailserver delivered to mailbox",
        container="mailserver",
        pattern=re.compile(r"to=<[^>]+>,.*status=sent"),
    ),
    Stage(
        key="scheduler_queued",
        label="Scheduler pulled and queued",
        container="b4igo-scheduler",
        pattern=re.compile(r"queued [1-9]\d* email\(s\) for"),
    ),
    Stage(
        key="ai_parsed",
        label="AI service parsed",
        container="ai-service",
        pattern=re.compile(r'POST /api/ai/text HTTP[^"]*"\s*2\d\d'),
    ),
    Stage(
        key="backend_enqueued",
        label="Backend enqueued confirmation",
        container="b4igo-backend",
        pattern=re.compile(r"enqueued confirmation id \d+ for user"),
        # If AI classified the email into a domain with no parser, the pipeline
        # legitimately produces zero confirmations. Watch ai-service for that
        # signal so the UI shows the skip rather than red-failing the stage.
        skip_pattern=re.compile(r"skipping unsupported domain"),
    ),
]


@dataclass
class StageEvent:
    """One stage transition reported back to the UI."""

    stage_key: str
    stage_label: str
    state: str  # "done" | "error"
    elapsed_ms: int
    sample_line: Optional[str] = None


@dataclass
class E2ERun:
    """Mutable state for one in-flight end-to-end pipeline test."""

    run_id: str
    since: int  # docker logs `since` (unix seconds, inclusive)
    queue: asyncio.Queue[StageEvent] = field(default_factory=asyncio.Queue)
    stages_done: set[str] = field(default_factory=set)
    tasks: list[asyncio.Task] = field(default_factory=list)
    start_time: float = field(default_factory=time.time)
    finished: bool = False

    def elapsed_ms(self) -> int:
        """Return milliseconds elapsed since the run started."""
        return int((time.time() - self.start_time) * 1000)


_runs: dict[str, E2ERun] = {}
_lock = asyncio.Lock()


def get_run(run_id: str) -> Optional[E2ERun]:
    """Return the run for the given id, or None if no such run exists."""
    return _runs.get(run_id)


async def _watch_pattern(
    stage: Stage,
    run: E2ERun,
    container: str,
    pattern: re.Pattern[str],
    state_on_match: str,
) -> None:
    """Tail one container's log stream until the pattern matches once."""
    try:
        async for line in docker_ops.stream_logs(container, since=run.since):
            if run.finished or stage.key in run.stages_done:
                return
            if pattern.search(line):
                run.stages_done.add(stage.key)
                await run.queue.put(
                    StageEvent(
                        stage_key=stage.key,
                        stage_label=stage.label,
                        state=state_on_match,
                        elapsed_ms=run.elapsed_ms(),
                        sample_line=line.strip(),
                    )
                )
                return
    except asyncio.CancelledError:
        raise
    except Exception as exc:
        logger.warning("stage %s watcher error: %s", stage.key, exc)
        await run.queue.put(
            StageEvent(
                stage_key=stage.key,
                stage_label=stage.label,
                state="error",
                elapsed_ms=run.elapsed_ms(),
                sample_line=f"watcher error: {exc}",
            )
        )


def _build_test_email(recipient: str, marker: str) -> MIMEText:
    # Content is intentionally health-domain heavy so the classifier reliably
    # routes it to a supported parser. The marker is included so the email is
    # identifiable in the mail server's logs.
    body = (
        "This is a friendly reminder of your medical appointment.\n\n"
        "Patient: Alice Demo\n"
        "Provider: Dr. Sarah Mitchell, MD (primary care physician)\n"
        "Clinic: Lakewood Family Medicine\n"
        "Date: Tuesday, June 17, 2026\n"
        "Time: 10:30 AM\n"
        "Location: 450 Oak Street, Suite 200, Lakewood\n"
        "Please bring your insurance card and a list of current medications.\n\n"
        f"Reference: e2e-test {marker}\n"
    )
    msg = MIMEText(body, "plain")
    msg["From"] = "appointments@lakewoodfamilymed.test.local"
    msg["To"] = recipient
    msg["Subject"] = f"Appointment reminder: Tuesday June 17 at 10:30 AM (e2e {marker})"
    return msg


async def start_run(
    mail_host: str,
    mail_port: int,
    recipient: str,
) -> E2ERun:
    """Cancel any active run, send the test email, and start fresh watchers."""
    async with _lock:
        for prior in list(_runs.values()):
            if not prior.finished:
                prior.finished = True
                for t in prior.tasks:
                    t.cancel()

        # Watchers must subscribe to logs *before* the SMTP send so we do not
        # miss the mailserver's delivery line. Use docker's `since` parameter
        # rooted just before now to capture the imminent activity.
        run = E2ERun(run_id=str(uuid.uuid4()), since=int(time.time()) - 1)
        _runs[run.run_id] = run

    # Spawn watchers first.
    for stage in STAGES:
        if stage.container and stage.pattern:
            run.tasks.append(
                asyncio.create_task(
                    _watch_pattern(stage, run, stage.container, stage.pattern, "done")
                )
            )
        # Optional skip pattern lives on ai-service today (it logs the
        # unsupported-domain skip line). Add a parallel watcher so either path
        # marks the stage terminal.
        if stage.skip_pattern:
            run.tasks.append(
                asyncio.create_task(
                    _watch_pattern(
                        stage, run, "ai-service", stage.skip_pattern, "skipped"
                    )
                )
            )

    # Trigger SMTP submit. Done synchronously in a thread so we do not block
    # the event loop on the SMTP handshake.
    marker = run.run_id[:8]
    msg = _build_test_email(recipient, marker)
    loop = asyncio.get_running_loop()

    def _send() -> None:
        with smtplib.SMTP(mail_host, mail_port, timeout=10) as smtp:
            smtp.send_message(msg)

    try:
        await loop.run_in_executor(None, _send)
        run.stages_done.add("smtp_submit")
        await run.queue.put(
            StageEvent(
                stage_key="smtp_submit",
                stage_label="SMTP submitted",
                state="done",
                elapsed_ms=run.elapsed_ms(),
                sample_line=f"sent to {recipient} (marker {marker})",
            )
        )
    except Exception as exc:
        run.stages_done.add("smtp_submit")
        await run.queue.put(
            StageEvent(
                stage_key="smtp_submit",
                stage_label="SMTP submitted",
                state="error",
                elapsed_ms=run.elapsed_ms(),
                sample_line=f"smtp error: {exc}",
            )
        )

    return run


async def stream_events(run: E2ERun) -> AsyncIterator[StageEvent]:
    """Yield stage events until the run completes or times out."""
    deadline = run.start_time + RUN_TIMEOUT_SECONDS
    expected = {s.key for s in STAGES}
    try:
        while True:
            remaining = max(0.5, deadline - time.time())
            try:
                evt = await asyncio.wait_for(run.queue.get(), timeout=remaining)
            except asyncio.TimeoutError:
                # Emit synthetic error events for any stage that did not fire,
                # so the UI can mark them red instead of leaving them spinning.
                for stage in STAGES:
                    if stage.key not in run.stages_done:
                        yield StageEvent(
                            stage_key=stage.key,
                            stage_label=stage.label,
                            state="error",
                            elapsed_ms=int((time.time() - run.start_time) * 1000),
                            sample_line="timed out",
                        )
                return
            yield evt
            if run.stages_done.issuperset(expected):
                return
    finally:
        run.finished = True
        for t in run.tasks:
            t.cancel()


def stages_for_template() -> list[dict[str, str]]:
    """Stage list shaped for the Jinja template."""
    return [{"key": s.key, "label": s.label} for s in STAGES]
