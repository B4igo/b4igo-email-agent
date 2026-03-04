from apscheduler.schedulers.background import BackgroundScheduler
import redis
import json
import time

queue = redis.Redis(host="localhost", port=6379, db=0, decode_responses=True)

#Job Processing
def queueProcessing():
    try:
        job = queue.lpop("confirmation_queue")
        if not job:
            print("no confirmations waiting")
            return
    
        job = json.loads(job)
        user = job["user"]
        payload = job["payload"]

        print(f"processing confirmation for {user}")
        print(payload)
      
        #TODO: pass new emails to ai subsystem

        print ("Done")
    
    except Exception as e:
        print("scheduler error: ",e)


scheduler = BackgroundScheduler()
scheduler.add_job(queueProcessing, "interval", seconds=10)
scheduler.start()

while True:
    time.sleep(60)
