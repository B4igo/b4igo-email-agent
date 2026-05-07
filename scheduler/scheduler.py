import base64
import json
import logging
import os
import sys
import time
from io import BytesIO

import redis
import requests
from apscheduler.schedulers.background import BackgroundScheduler
from flask import Flask, jsonify, request

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)],
)
logger = logging.getLogger("scheduler")

# Service endpoints, configurable via env so the same code runs locally and in compose.
AI_SERVICE_URL = os.environ.get("B4IGO_AI_SERVICE_URL", "http://localhost:5300").rstrip("/")
ACCOUNT_MANAGER_URL = os.environ.get(
    "B4IGO_ACCOUNT_MANAGER_URL", "http://localhost:5100"
).rstrip("/")
REDIS_HOST = os.environ.get("REDIS_HOST", "localhost")
REDIS_PORT = int(os.environ.get("REDIS_PORT", "6379"))
POLL_INTERVAL_SECONDS = int(os.environ.get("POLL_INTERVAL_SECONDS", "10"))
QUEUE_INTERVAL_SECONDS = int(os.environ.get("QUEUE_INTERVAL_SECONDS", "2"))

aiCallText = f"{AI_SERVICE_URL}/api/ai/text"
aiCallAttachments = f"{AI_SERVICE_URL}/api/ai/text-with-attachments"
accountEmailCall = f"{ACCOUNT_MANAGER_URL}/api/pull"

# Redis Connection Setup------------------------------
queue = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, db=0, decode_responses=True)
MainQueue = "mail_pull_queue"
AccountQueue = "account_registry_queue"
DeadQueue = "dead_mail_queue"

# Flask Endpoint to receive new account registries
app = Flask(__name__)


@app.route("/api/scheduler/registry", methods=["POST"])
def registerAccount():
    """Register one linked account for periodic polling."""
    data = request.get_json(silent=True) or {}

    required = ["b4igoUserId", "accountId"]
    if any(field not in data for field in required):
        return jsonify({"error": "Required fields missing"}), 400

    account = {"b4igoUserId": data["b4igoUserId"], "accountId": data["accountId"]}
    queue.sadd(AccountQueue, json.dumps(account))

    return jsonify({"message": "Registered for polling", "account": account}), 201


# Schedule Processing---------------------------
def pollToQueue():
    """Poll account-manager for new emails and queue them in Redis."""
    try:
        logger.info("starting poll cycle")

        # pull registered accounts from redis
        accounts = queue.smembers(AccountQueue)

        for accountJson in accounts:
            account = json.loads(accountJson)

            user = account["b4igoUserId"]
            accountId = account["accountId"]

            response = requests.post(
                accountEmailCall,
                json={"b4igoUserId": user, "accountIds": [accountId]},
                timeout=10,
            )
            if response.status_code != 200:
                logger.warning(
                    "pull failed for user %s: status %s", user, response.status_code
                )
                continue
            try:
                payload = response.json()
            except Exception as exc:
                logger.warning("pull response parse failed for user %s: %s", user, exc)
                continue
            # /api/pull returns {"emails": [...], "errors": [...], "accountsPolled": N}
            emails = payload.get("emails", []) if isinstance(payload, dict) else []
            errors = payload.get("errors", []) if isinstance(payload, dict) else []
            for err in errors:
                logger.warning(
                    "provider pull error for user %s account %s: %s",
                    user,
                    err.get("accountId"),
                    err.get("error"),
                )

            for email in emails:
                metadata = email.get("metadata") or {}
                job = {
                    "user": user,
                    "accountId": accountId,
                    "retry": 0,
                    "email": {
                        "subject": email.get("subject", ""),
                        "from": metadata.get("from", ""),
                        "body": email.get("body", ""),
                        "attachments": email.get("attachments", []),
                    },
                }
                queue.rpush(MainQueue, json.dumps(job))
                logger.info("enqueued job %s", json.dumps(job))

            logger.info("queued %d email(s) for user %s", len(emails), user)
    except Exception as exc:
        logger.exception("poll cycle failed: %s", exc)


def queueProcessing():
    """Pop one queued email from Redis and hand it off to ai-service."""
    job = None
    try:
        job = queue.lpop(MainQueue)
        if not job:
            logger.debug("no jobs waiting")
            return

        jobData = json.loads(job)

        logger.info(
            "processing job for user %s account %s subject=%r",
            jobData["user"],
            jobData["accountId"],
            jobData.get("email", {}).get("subject", ""),
        )

        email = jobData.get("email", {})
        text = (
            f"From: {email.get('from', '')}\n"
            f"Subject: {email.get('subject', '')}\n\n"
            f"{email.get('body', '')}"
        )
        attachments = email.get("attachments") or []

        # Each attachment is expected as {filename, content_type, content_b64}
        # produced by the imap provider. Base64 is used so the dict survives
        # JSON serialisation through Redis. Decode here back to raw bytes for
        # the multipart upload to ai-service.
        normalized_files = []
        for i, att in enumerate(attachments):
            if not isinstance(att, dict):
                continue
            filename = att.get("filename") or f"attachment_{i}"
            content_type = att.get("content_type") or "application/octet-stream"
            try:
                raw = base64.b64decode(att.get("content_b64", ""))
            except (ValueError, TypeError):
                logger.warning(
                    "skipping attachment %s with invalid content_b64", filename
                )
                continue
            normalized_files.append(("files", (filename, BytesIO(raw), content_type)))

        if not normalized_files:
            response = requests.post(
                aiCallText,
                json={"text": text, "username": jobData["user"]},
                timeout=300,
            )
        else:
            response = requests.post(
                aiCallAttachments,
                data={"text": text, "username": jobData["user"]},
                files=normalized_files,
                timeout=300,
            )

        if response.status_code in (200, 201, 202):
            logger.info(
                "ai handoff succeeded for user %s account %s",
                jobData["user"],
                jobData["accountId"],
            )
        else:
            jobData["retry"] += 1
            if jobData["retry"] >= 3:
                logger.warning(
                    "ai handoff exhausted retries for user %s account %s,"
                    " sending to dead queue",
                    jobData["user"],
                    jobData["accountId"],
                )
                queue.rpush(DeadQueue, json.dumps(jobData))
            else:
                logger.warning(
                    "ai handoff failed status %s for user %s, retrying (%d/3)",
                    response.status_code,
                    jobData["user"],
                    jobData["retry"],
                )
                queue.rpush(MainQueue, json.dumps(jobData))

    except Exception as exc:
        logger.exception("queue processing failed: %s", exc)
        # if a job was dequeued put it back
        if job:
            queue.rpush(MainQueue, job)

@app.route("/api/health", methods=["GET"])
def health_check():
    """Health check endpoint for account manager service."""
    return jsonify({"status": "healthy", "service": "scheduler"}), 200

#Setup Scheduler--------------------------
scheduler = BackgroundScheduler()
scheduler.add_job(queueProcessing, "interval", seconds=QUEUE_INTERVAL_SECONDS)
scheduler.add_job(pollToQueue, "interval", seconds=POLL_INTERVAL_SECONDS)
scheduler.start()
logger.info(
    "scheduler started: poll=%ss queue=%ss ai=%s account_manager=%s redis=%s:%d",
    POLL_INTERVAL_SECONDS,
    QUEUE_INTERVAL_SECONDS,
    AI_SERVICE_URL,
    ACCOUNT_MANAGER_URL,
    REDIS_HOST,
    REDIS_PORT,
)

# start Flask
app.run(host="0.0.0.0", port=5200)

while True:
    time.sleep(60)
