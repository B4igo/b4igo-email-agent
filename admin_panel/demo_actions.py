"""Demo-only actions: clear queue, send mail, run scenarios, reset."""

from __future__ import annotations

import json
import logging
import mimetypes
import smtplib
from dataclasses import dataclass, field
from email.mime.application import MIMEApplication
from email.mime.audio import MIMEAudio
from email.mime.base import MIMEBase
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from pathlib import Path
from typing import Iterable, Optional

import docker_ops
import requests
from config import (
    BACKEND_ADMIN_TOKEN,
    BACKEND_URL,
    MAIL_DOMAIN,
    MAIL_HOST,
    MAIL_SMTP_PORT,
)

logger = logging.getLogger("admin-panel")

SEED_ACCOUNTS = [
    "alice@test.local",
    "bob@test.local",
    "charlie@test.local",
    "diana@test.local",
    "eve@test.local",
]

SCENARIOS_DIR = Path(__file__).parent / "scenarios"


@dataclass
class Scenario:
    """One preset email scenario sendable from the admin panel demo page."""

    key: str
    label: str
    sender_name: str
    sender_local: str
    subject: str
    body: str
    # Resolved absolute paths to attachment files. The on-disk JSON stores
    # them as paths relative to the scenario file's directory.
    attachments: list[Path] = field(default_factory=list)


def _load_scenarios() -> list[Scenario]:
    """Load every scenarios/*.json file at module import time.

    The filename (sans .json) is the scenario key, so adding a new test email
    is a single new file and no Python changes. Attachment paths in the JSON
    are resolved relative to the JSON file's parent directory.
    """
    scenarios: list[Scenario] = []
    if not SCENARIOS_DIR.exists():
        logger.warning("scenarios directory %s missing", SCENARIOS_DIR)
        return scenarios

    for path in sorted(SCENARIOS_DIR.glob("*.json")):
        try:
            data = json.loads(path.read_text())
        except (OSError, json.JSONDecodeError) as exc:
            logger.warning("skipping %s: %s", path.name, exc)
            continue

        attachments: list[Path] = []
        for rel in data.get("attachments", []) or []:
            resolved = (path.parent / rel).resolve()
            if not resolved.is_file():
                logger.warning(
                    "scenario %s references missing attachment %s",
                    path.stem,
                    resolved,
                )
                continue
            attachments.append(resolved)

        scenarios.append(
            Scenario(
                key=path.stem,
                label=data.get("label", path.stem),
                sender_name=data.get("from_name", ""),
                sender_local=data.get("from_local", "no-reply"),
                subject=data.get("subject", ""),
                body=data.get("body", ""),
                attachments=attachments,
            )
        )
    return scenarios


SCENARIOS: list[Scenario] = _load_scenarios()


def scenarios_by_key() -> dict[str, Scenario]:
    """Return scenarios indexed by their key."""
    return {s.key: s for s in SCENARIOS}


# ---- Confirmation queue ----


def clear_queue(username: Optional[str] = None) -> tuple[bool, str]:
    """Clear the backend confirmation queue via the admin endpoint."""
    if not BACKEND_ADMIN_TOKEN:
        return False, "B4IGO_ADMIN_TOKEN not set on backend; admin endpoint disabled."
    url = f"{BACKEND_URL}/api/confirmations/admin/clear"
    params = {"username": username} if username else None
    try:
        r = requests.delete(
            url,
            params=params,
            headers={"X-Admin-Token": BACKEND_ADMIN_TOKEN},
            timeout=10,
        )
    except requests.RequestException as e:
        return False, f"Backend unreachable: {e}"
    if r.status_code != 200:
        return False, f"Backend returned {r.status_code}: {r.text}"
    return True, f"Deleted {r.json().get('deleted', 0)} confirmation(s)."


# ---- SMTP helpers ----


def _smtp_send(messages: Iterable[tuple[str, str, MIMEMultipart]]) -> int:
    """Send a batch of (from, to, message) tuples through one SMTP connection."""
    sent = 0
    with smtplib.SMTP(MAIL_HOST, MAIL_SMTP_PORT, timeout=15) as smtp:
        for sender, recipient, msg in messages:
            smtp.sendmail(sender, [recipient], msg.as_string())
            sent += 1
    return sent


def _attach_file(msg: MIMEMultipart, path: Path) -> None:
    """Attach one file to a multipart message, picking the right MIME class."""
    ctype, encoding = mimetypes.guess_type(str(path))
    if ctype is None or encoding is not None:
        ctype = "application/octet-stream"
    maintype, subtype = ctype.split("/", 1)
    data = path.read_bytes()

    part: MIMEBase
    if maintype == "text":
        try:
            text = data.decode("utf-8")
        except UnicodeDecodeError:
            text = data.decode("utf-8", errors="replace")
        part = MIMEText(text, subtype)
    elif maintype == "image":
        part = MIMEImage(data, subtype)
    elif maintype == "audio":
        part = MIMEAudio(data, subtype)
    else:
        part = MIMEApplication(data, subtype)

    part.add_header("Content-Disposition", "attachment", filename=path.name)
    msg.attach(part)


def _build(
    sender_name: str,
    sender_addr: str,
    recipient: str,
    subject: str,
    body: str,
    attachments: Optional[list[Path]] = None,
) -> MIMEMultipart:
    msg = MIMEMultipart()
    msg["From"] = f"{sender_name} <{sender_addr}>" if sender_name else sender_addr
    msg["To"] = recipient
    msg["Subject"] = subject
    msg.attach(MIMEText(body, "plain"))
    for path in attachments or []:
        _attach_file(msg, path)
    return msg


def send_scenario(scenario_key: str, recipient: str) -> tuple[bool, str]:
    """Send one preset scenario email to a recipient."""
    s = scenarios_by_key().get(scenario_key)
    if s is None:
        return False, f"Unknown scenario: {scenario_key}"
    sender_addr = f"{s.sender_local}@{MAIL_DOMAIN}"
    msg = _build(
        s.sender_name, sender_addr, recipient, s.subject, s.body, s.attachments
    )
    try:
        _smtp_send([(sender_addr, recipient, msg)])
    except Exception as e:
        return False, f"SMTP error: {e}"
    suffix = f" with {len(s.attachments)} attachment(s)" if s.attachments else ""
    return True, f"Sent '{s.label}' to {recipient}{suffix}."


def send_bulk(count: int, recipient: str) -> tuple[bool, str]:
    """Send N preset emails (cycling through scenarios) to a recipient."""
    if count <= 0 or count > 100:
        return False, "Count must be between 1 and 100."
    scenarios = SCENARIOS
    msgs: list[tuple[str, str, MIMEMultipart]] = []
    for i in range(count):
        s = scenarios[i % len(scenarios)]
        sender_addr = f"{s.sender_local}@{MAIL_DOMAIN}"
        subject = f"{s.subject} (#{i + 1})"
        msgs.append(
            (
                sender_addr,
                recipient,
                _build(
                    s.sender_name,
                    sender_addr,
                    recipient,
                    subject,
                    s.body,
                    s.attachments,
                ),
            )
        )
    try:
        sent = _smtp_send(msgs)
    except Exception as e:
        return False, f"SMTP error after sending some messages: {e}"
    return True, f"Sent {sent} email(s) to {recipient}."


def send_custom(
    sender: str, recipient: str, subject: str, body: str
) -> tuple[bool, str]:
    """Send one custom email with the given subject and body."""
    if "@" not in sender or "@" not in recipient:
        return False, "Sender and recipient must be email addresses."
    msg = _build("", sender, recipient, subject, body)
    try:
        _smtp_send([(sender, recipient, msg)])
    except Exception as e:
        return False, f"SMTP error: {e}"
    return True, f"Sent custom email from {sender} to {recipient}."


# ---- One-click reset ----


def one_click_reset() -> tuple[bool, list[str]]:
    """Drain in-flight pipeline state for a fresh demo run.

    Wipes the backend confirmation queue and the scheduler's transient Redis
    queues (mail_pull_queue, dead_mail_queue), then restarts the backend so any
    in-memory state is cleared. We deliberately do *not* drop the maildata
    volume or the linked-account registry - a full data wipe requires
    `docker compose down -v`, which can't be triggered from inside a container.
    """
    log: list[str] = []

    ok, msg = clear_queue()
    log.append(f"Clear confirmations queue: {msg}")

    redis = docker_ops.safe_get("b4igo-redis")
    if redis is not None:
        try:
            res = redis.exec_run(
                ["redis-cli", "DEL", "mail_pull_queue", "dead_mail_queue"]
            )
            removed = res.output.decode("utf-8", errors="replace").strip()
            log.append(
                "cleared scheduler queues "
                f"(mail_pull_queue, dead_mail_queue): {removed} key(s)"
            )
        except Exception as e:
            log.append(f"Could not clear scheduler queues: {e}")

    for name in ("b4igo-backend",):
        c = docker_ops.safe_get(name)
        if c is not None:
            try:
                c.restart(timeout=10)
                log.append(f"Restarted {name}.")
            except Exception as e:
                log.append(f"Failed to restart {name}: {e}")

    return True, log


# ---- AI playground ----


def ai_dry_run(text: str) -> tuple[bool, dict | str]:
    """Run text through the AI service in dry-run mode and return the parsed entries."""
    from config import AI_SERVICE_URL

    try:
        r = requests.post(
            f"{AI_SERVICE_URL}/api/ai/text",
            json={"text": text, "username": "__playground__", "dry_run": True},
            timeout=300,
        )
    except requests.RequestException as e:
        return False, f"AI service unreachable: {e}"
    if r.status_code >= 400:
        return False, f"AI service returned {r.status_code}: {r.text}"
    try:
        return True, r.json()
    except ValueError:
        return False, f"Invalid JSON from AI service: {r.text[:500]}"
