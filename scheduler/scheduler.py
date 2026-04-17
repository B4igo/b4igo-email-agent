from apscheduler.schedulers.background import BackgroundScheduler
import redis
import json
import time
import requests  
from flask import Flask, request, jsonify
from io import BytesIO

# API Endpoints
aiCallText = "http://localhost:5300/api/ai/text"
aiCallAttachments = "http://localhost:5300/api/ai/text-with-attachments"
accountEmailCall = "http://localhost:5100/api/pull"

#Redis Connection Setup------------------------------
queue = redis.Redis(
    host="localhost",
    port=6379, 
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
                emails = response.json()
            except Exception as e:
                print ("Polling email error", e)
                continue
            if not isinstance(emails, list):
                continue

            for email in emails:
                job={"user":user, 
                     "accountId": accountId, 
                     "retry": 0,
                     "email":{
                         "subject": email.get("subject",""),
                         "from": email.get("from",""),
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
                aiCallText, json={"text":text}, timeout=10)
        else:
            response = requests.post(
                aiCallAttachments, 
                data={"text":text},
                files=normalized_files, 
                timeout=10
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
scheduler.add_job(queueProcessing, "interval", seconds=5,)
scheduler.add_job(pollToQueue, "interval", seconds=40,)
scheduler.start()
print("Starting Scheduler...")

#start Flask
app.run(host="0.0.0.0", port=5200)

while True:
    time.sleep(60)
