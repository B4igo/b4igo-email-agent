from apscheduler.schedulers.background import BackgroundScheduler
import os
import redis
import json
import time
import requests
from flask import Flask, request, jsonify
from io import BytesIO

# Service endpoints — configurable via env so the same code runs locally and in compose.
AI_SERVICE_URL = os.environ.get("AI_SERVICE_URL", "http://localhost:5300").rstrip("/")
ACCOUNT_MANAGER_URL = os.environ.get("ACCOUNT_MANAGER_URL", "http://localhost:5100").rstrip("/")
REDIS_HOST = os.environ.get("REDIS_HOST", "localhost")
REDIS_PORT = int(os.environ.get("REDIS_PORT", "6379"))
POLL_INTERVAL_SECONDS = int(os.environ.get("POLL_INTERVAL_SECONDS", "30"))
QUEUE_INTERVAL_SECONDS = int(os.environ.get("QUEUE_INTERVAL_SECONDS", "5"))

aiCallText = f"{AI_SERVICE_URL}/api/ai/text"
aiCallAttachments = f"{AI_SERVICE_URL}/api/ai/text-with-attachments"
accountEmailCall = f"{ACCOUNT_MANAGER_URL}/api/pull"

#Redis Connection Setup------------------------------
queue = redis.Redis(
    host=REDIS_HOST,
    port=REDIS_PORT,
    db=0,
    decode_responses=True)
MainQueue = "mail_pull_queue"
AccountQueue = "account_registry_queue"
DeadQueue = "dead_mail_queue"

#Flask Endpoint to receive new account registries
app = Flask(__name__)

@app.route("/api/scheduler/registry", methods=["POST"])
def registerAccount():
    data = request.get_json(silent=True) or {}

    required = ["b4igoUserId", "accountId"]
    if any(field not in data for field in required):
        return jsonify({"error": "Required fields missing"}), 400

    account = {
        "b4igoUserId": data["b4igoUserId"],
        "accountId": data["accountId"]
    }
    queue.sadd(AccountQueue, json.dumps(account))

    return jsonify ({
        "message": "Registered for polling",
        "account": account 
    }),201

#Schedule Processing---------------------------
def pollToQueue():
    try:
        print("Starting poll")

        #pull registered accounts from redis
        accounts = queue.smembers(AccountQueue)

        for accountJson in accounts:
            account = json.loads(accountJson)

            user = account["b4igoUserId"]
            accountId = account["accountId"]

            response = requests.post(
                accountEmailCall,
                json={"b4igoUserId": user, "accountIds": [accountId]},
                timeout=10
            )
            if response.status_code != 200:
                print(f"Poll failed for {user}")
                continue
            try:
                payload = response.json()
            except Exception as e:
                print ("Polling email error", e)
                continue
            # /api/pull returns {"emails": [...], "errors": [...], "accountsPolled": N}
            emails = payload.get("emails", []) if isinstance(payload, dict) else []
            errors = payload.get("errors", []) if isinstance(payload, dict) else []
            for err in errors:
                print(f"Pull error for {user} account {err.get('accountId')}: {err.get('error')}")

            for email in emails:
                metadata = email.get("metadata") or {}
                job={"user":user,
                     "accountId": accountId,
                     "retry": 0,
                     "email":{
                         "subject": email.get("subject",""),
                         "from": metadata.get("from", ""),
                         "body": email.get("body",""),
                         "attachments": email.get("attachments", [])
                     }
                }
                queue.rpush(MainQueue,json.dumps(job))

            print(f"{len(emails)} emails queued for {user}")
    except Exception as e:
        print("Polling error", e)

def queueProcessing():
    job = None
    try:
        job = queue.lpop(MainQueue)
        if not job:
            print("No jobs waiting.")
            return
        
        jobData = json.loads(job)
        
        print(f"Processing job for {jobData['user']}: ")
        print(json.dumps(jobData, indent=2))

        email = jobData.get("email", {})
        text = f""" 
        From: {email.get('from','')}
        Subject: {email.get('subject','')}

        {email.get('body','')}
        """
        attachments = email.get("attachments") or []

        normalized_files = []
        for i, att in enumerate(attachments):
            if isinstance(att, dict):
                filename = att.get("filename", f"attachment_{i}.txt")
                content = att.get("content", "")
            else:
                filename = f"attachment_{i}.txt"
                content = str(att)
            normalized_files.append((
                "files", (filename, BytesIO(content.encode()))
                ))

        if not normalized_files:
            response = requests.post(
                aiCallText,
                json={"text": text, "username": jobData["user"]},
                timeout=300)
        else:
            response = requests.post(
                aiCallAttachments,
                data={"text": text, "username": jobData["user"]},
                files=normalized_files,
                timeout=300
                )
            
        if response.status_code in (200,201,202):
            print(f"Ai processing successful user:{jobData['user']} Account:{jobData['accountId']}")
        else:
            jobData["retry"] += 1
            if jobData["retry"] >=3:
                print("Sending to Dead queue")
                queue.rpush(DeadQueue, json.dumps(jobData))
            else:
                print (f"Processing failed retrying job({jobData['retry']})")
                queue.rpush(MainQueue, json.dumps(jobData))

    except Exception as e:
        print ("AI processing error", e) 
        #if a job was dequeued put it back
        if job:
            queue.rpush(MainQueue, job)
        
#Setup Scheduler--------------------------
scheduler = BackgroundScheduler()
scheduler.add_job(queueProcessing, "interval", seconds=QUEUE_INTERVAL_SECONDS)
scheduler.add_job(pollToQueue, "interval", seconds=POLL_INTERVAL_SECONDS)
scheduler.start()
print("Starting Scheduler...")

#start Flask
app.run(host="0.0.0.0", port=5200)

while True:
    time.sleep(60)
