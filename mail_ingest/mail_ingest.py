#!/usr/bin/env python3
"""Read emails from IMAP mailbox and feed them through the b4igo AI pipeline.

Connects to the mail server, fetches unseen emails for a configured account,
classifies and parses them, then enqueues confirmations via the backend API.
"""

import email
import email.policy
import email.utils
import imaplib
import json
import logging
import os
import re
import sys
import time
from datetime import datetime
from email.message import EmailMessage

import requests

from shared.mail.models import EmailAddress, EmailInput

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)],
)
logger = logging.getLogger(__name__)

# Configuration via environment variables
IMAP_HOST = os.environ.get("IMAP_HOST", "mailserver")
IMAP_PORT = int(os.environ.get("IMAP_PORT", "143"))
IMAP_USER = os.environ.get("IMAP_USER", "alice@test.local")
IMAP_PASS = os.environ.get("IMAP_PASS", "password123")

BACKEND_URL = os.environ.get("BACKEND_URL", "http://backend:5000")
BACKEND_USER = os.environ.get("BACKEND_USER", "user")

POLL_INTERVAL = int(os.environ.get("POLL_INTERVAL", "0"))  # 0 = run once


def wait_for_service(name: str, check_fn, retries: int = 90, delay: float = 3.0):
    """Block until a service is reachable."""
    for attempt in range(retries):
        try:
            check_fn()
            logger.info("%s is ready", name)
            return
        except Exception as e:
            logger.info("Waiting for %s (%d/%d): %s", name, attempt + 1, retries, e)
            time.sleep(delay)
    raise RuntimeError(f"{name} not available after {retries} attempts")


def check_imap():
    """Verify IMAP is accepting connections and login works."""
    conn = imaplib.IMAP4(IMAP_HOST, IMAP_PORT)
    conn.login(IMAP_USER, IMAP_PASS)
    conn.logout()


def check_backend():
    """Verify the backend health endpoint responds."""
    resp = requests.get(f"{BACKEND_URL}/api/health", timeout=5)
    resp.raise_for_status()


def check_ollama():
    """Verify Ollama has the required model available."""
    ollama_host = os.environ.get("OLLAMA_HOST", "http://ollama:11434")
    resp = requests.get(f"{ollama_host}/api/tags", timeout=5)
    resp.raise_for_status()
    models = [m["name"] for m in resp.json().get("models", [])]
    if not any("qwen3" in m for m in models):
        raise RuntimeError(f"qwen3:8b not found in Ollama models: {models}")


def parse_address(raw: str) -> EmailAddress:
    """Parse an email address string, tolerating .local TLDs.

    Pydantic's EmailStr rejects .local domains, so we construct
    EmailAddress with model_construct() to skip validation.
    """
    raw = str(raw).strip()
    # "Name <addr>" format
    match = re.match(r"^(.*?)\s*<([^>]+)>", raw)
    if match:
        name = match.group(1).strip().strip("\"'") or None
        addr = match.group(2).strip()
    elif "@" in raw:
        name = None
        addr = raw
    else:
        # display name only, no address
        name = raw
        addr = f"{raw.lower().replace(' ', '')}@unknown"

    return EmailAddress.model_construct(address=addr, name=name)


def mime_to_email_input(msg: EmailMessage) -> EmailInput:
    """Convert a stdlib EmailMessage to EmailInput, bypassing EmailStr validation.

    Uses model_construct() to skip Pydantic validation so .local domains work.
    """
    from_raw = str(msg.get("from", ""))
    from_addr = parse_address(from_raw)

    to_raw = str(msg.get("to", ""))
    to_addrs = [parse_address(a.strip()) for a in to_raw.split(",") if a.strip()]

    subject = str(msg.get("subject", ""))

    # Extract body
    body = ""
    if msg.is_multipart():
        for part in msg.walk():
            ct = part.get_content_type()
            if ct == "text/plain":
                body = part.get_content()
                break
    else:
        body = msg.get_content()

    # Parse date
    date_str = msg.get("date")
    try:
        received_at = (
            email.utils.parsedate_to_datetime(date_str) if date_str else datetime.now()
        )
    except Exception:
        received_at = datetime.now()

    return EmailInput.model_construct(
        from_address=from_addr,
        to_address=to_addrs,
        subject=subject,
        body=body or "",
        received_at=received_at,
        cc=[],
        bcc=[],
        metadata=None,
        attachments=[],
    )


def fetch_emails() -> list[EmailMessage]:
    """Fetch all emails from the IMAP mailbox."""
    conn = imaplib.IMAP4(IMAP_HOST, IMAP_PORT)
    conn.login(IMAP_USER, IMAP_PASS)
    conn.select("INBOX")

    # Fetch all messages (for demo purposes)
    status, data = conn.search(None, "ALL")
    if status != "OK" or not data[0]:
        logger.info("No emails found in mailbox")
        conn.logout()
        return []

    msg_ids = data[0].split()
    logger.info("Found %d emails in mailbox", len(msg_ids))

    messages: list[EmailMessage] = []
    for msg_id in msg_ids:
        status, msg_data = conn.fetch(msg_id, "(RFC822)")
        if status != "OK":
            continue
        raw_email = msg_data[0][1]
        msg = email.message_from_bytes(raw_email, policy=email.policy.default)
        messages.append(msg)

    conn.logout()
    return messages


def enqueue_confirmation(username: str, payload: str):
    """POST a confirmation to the backend API."""
    resp = requests.post(
        f"{BACKEND_URL}/api/confirmations/enqueue",
        json={"username": username, "jsonPayload": payload},
        timeout=30,
    )
    if resp.status_code == 201:
        logger.info("Enqueued confirmation for %s", username)
    else:
        logger.warning(
            "Failed to enqueue confirmation: %s %s", resp.status_code, resp.text
        )


def call_ai_pipeline(email_input: EmailInput) -> list[dict[str, dict]]:
    resp = requests.post(
        f"{BACKEND_URL}/api/ai/text",
        json={
            "username": BACKEND_USER,
            "jsonPayload": email_input.model_dump_json(),
        },
        timeout=30,
    )
    if resp.status_code == 201:
        logger.info("Called AI service for %s", BACKEND_USER)
        return resp.json()["data"]
    else:
        logger.warning("Failed to call AI service: %s %s", resp.status_code, resp.text)
        return []


def process_emails():
    """Main pipeline: fetch → parse → enqueue."""
    raw_messages = fetch_emails()
    if not raw_messages:
        logger.info("No emails to process")
        return

    # Convert to EmailInput (using model_construct to bypass .local TLD validation)
    email_inputs: list[EmailInput] = []
    for msg in raw_messages:
        try:
            email_input = mime_to_email_input(msg)
            email_inputs.append(email_input)
        except Exception as e:
            logger.warning("Skipping malformed email: %s", e)

    logger.info("Converted %d emails to EmailInput", len(email_inputs))

    # Parse all emails
    for email_input in email_inputs:
        parsed_entries = call_ai_pipeline(email_input)
        for entry in parsed_entries:
            enqueue_confirmation(BACKEND_URL, json.dumps(entry))


def main():
    logger.info("B4iGO Mail Ingest starting")
    logger.info(
        "Config: IMAP=%s:%d user=%s backend=%s",
        IMAP_HOST,
        IMAP_PORT,
        IMAP_USER,
        BACKEND_URL,
    )

    # Wait for all services
    wait_for_service("IMAP", check_imap)
    wait_for_service("Backend", check_backend)
    wait_for_service("Ollama (with model)", check_ollama, retries=120, delay=5.0)

    if POLL_INTERVAL > 0:
        logger.info("Polling every %d seconds", POLL_INTERVAL)
        while True:
            process_emails()
            time.sleep(POLL_INTERVAL)
    else:
        process_emails()
        logger.info("Single run complete, exiting")


if __name__ == "__main__":
    main()
