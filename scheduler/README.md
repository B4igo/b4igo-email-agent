# scheduler

Flask service (port 5200) with a background APScheduler worker. It drives the
pipeline: it polls account-manager for new mail, queues it in Redis, and hands each
message to ai-service.

## Responsibilities

- Account registry: `POST /api/scheduler/registry` enrolls an account for polling.
- Polling: every `POLL_INTERVAL_SECONDS`, calls account-manager `POST /api/pull` for
  each registered account and pushes new messages onto the Redis `mail_pull_queue`.
- Handoff: every `QUEUE_INTERVAL_SECONDS`, drains the queue and posts each message to
  ai-service `POST /api/ai/text` (or `/api/ai/text-with-attachments` when the message
  has decoded attachments).
- Reliability: retries the AI handoff up to three times, then parks the job in a
  dead-letter queue.

## Key endpoints

| Method | Path | Purpose |
|---|---|---|
| POST | `/api/scheduler/registry` | Enroll an account for polling |
| GET | `/api/health` | Liveness check |

## Configuration

`REDIS_HOST`, `REDIS_PORT`, `B4IGO_ACCOUNT_MANAGER_URL`, `B4IGO_AI_SERVICE_URL`,
`POLL_INTERVAL_SECONDS`, `QUEUE_INTERVAL_SECONDS`. See `docs/CONFIGURATION.md`. Use a
poll interval of 60 to 300 seconds in production to respect provider rate limits; the
demo uses 5 seconds.

## Run standalone

```bash
pip install -r scheduler/requirements.txt
# requires a reachable Redis, account-manager, and ai-service
python scheduler/scheduler.py
```

## Tests

No automated tests yet (see `docs/ROADMAP.md`).
