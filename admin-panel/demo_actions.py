"""Demo-only actions: clear queue, send mail, run scenarios, reset."""

from __future__ import annotations

import smtplib
from dataclasses import dataclass
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
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

SEED_ACCOUNTS = [
    "alice@test.local",
    "bob@test.local",
    "charlie@test.local",
    "diana@test.local",
    "eve@test.local",
]


@dataclass
class Scenario:
    """One preset email scenario sendable from the admin panel demo page."""

    key: str
    label: str
    sender_name: str
    sender_local: str
    subject: str
    body: str


SCENARIOS: list[Scenario] = [
    Scenario(
        key="appointment",
        label="Doctor appointment reminder",
        sender_name="Dr. Sarah Mitchell - Lakewood Family Medicine",
        sender_local="appointments@lakewoodfamilymed",
        subject="Appointment Reminder: Tuesday, March 24 at 10:30 AM",
        body=(
            "This is a reminder that you have an upcoming appointment.\n\n"
            "Provider: Dr. Sarah Mitchell\n"
            "Date: Tuesday, March 24, 2026\n"
            "Time: 10:30 AM\n"
            "Location: Lakewood Family Medicine, 450 Oak Street, Suite 200\n"
        ),
    ),
    Scenario(
        key="shipping",
        label="Shipping notification (Amazon)",
        sender_name="Amazon.com",
        sender_local="shipment-tracking@amazon",
        subject="Your Amazon order has shipped!",
        body=(
            "Order #112-9374856-2938471\n"
            "Carrier: UPS\n"
            "Tracking: 1Z999AA10123456784\n"
            "Estimated delivery: March 19-21, 2026\n"
        ),
    ),
    Scenario(
        key="password_reset",
        label="Password reset (GitHub)",
        sender_name="GitHub",
        sender_local="noreply@github",
        subject="[GitHub] Password reset request",
        body=(
            "We received a request to reset the password for your account.\n"
            "If you made this request, click below within 24 hours:\n"
            "https://github.example.com/password_reset/abc123def456\n"
        ),
    ),
    Scenario(
        key="bill",
        label="Utility bill due (PG&E)",
        sender_name="Pacific Gas & Electric",
        sender_local="notifications@pge",
        subject="Your electricity bill is due March 28",
        body=(
            "Account Number: ****6739\n"
            "Amount Due: $142.37\n"
            "Due Date: March 28, 2026\n"
        ),
    ),
    Scenario(
        key="meeting",
        label="Zoom meeting reminder",
        sender_name="Zoom",
        sender_local="no-reply@zoom",
        subject="Reminder: Team Standup starts in 15 minutes",
        body=(
            "Topic: Team Standup\n"
            "Time: March 16, 2026 09:00 AM (Mountain Time)\n"
            "Join: https://zoom.example.com/j/98765432100?pwd=abcDEF123\n"
        ),
    ),
]


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


def _build(
    sender_name: str, sender_addr: str, recipient: str, subject: str, body: str
) -> MIMEMultipart:
    msg = MIMEMultipart()
    msg["From"] = f"{sender_name} <{sender_addr}>" if sender_name else sender_addr
    msg["To"] = recipient
    msg["Subject"] = subject
    msg.attach(MIMEText(body, "plain"))
    return msg


def send_scenario(scenario_key: str, recipient: str) -> tuple[bool, str]:
    """Send one preset scenario email to a recipient."""
    s = scenarios_by_key().get(scenario_key)
    if s is None:
        return False, f"Unknown scenario: {scenario_key}"
    sender_addr = f"{s.sender_local}@{MAIL_DOMAIN}"
    msg = _build(s.sender_name, sender_addr, recipient, s.subject, s.body)
    try:
        _smtp_send([(sender_addr, recipient, msg)])
    except Exception as e:
        return False, f"SMTP error: {e}"
    return True, f"Sent '{s.label}' to {recipient}."


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
                _build(s.sender_name, sender_addr, recipient, subject, s.body),
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
    volume or the linked-account registry — a full data wipe requires
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
