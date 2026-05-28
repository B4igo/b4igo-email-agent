# admin-panel (demo only)

FastAPI service (port 5400) that provides an operations UI for the demo stack. It is
not part of a production deployment: it mounts the Docker socket to inspect and drive
the other containers, so it is bound to `127.0.0.1` only.

## Features

- **Pipeline trace**: combined live log stream from each pipeline stage.
- **Demo actions**: send canned scenarios or custom emails to a seed mailbox, clear
  the confirmation queue, and reset state.
- **End-to-end test**: drop one synthetic email and watch each stage flip green based
  on its container's logs. A smoke test for the whole pipeline.
- **AI playground**: feed arbitrary text through the AI pipeline in dry-run mode and
  see the parsed entries without enqueuing them.

## Why it is demo only

`docker_ops.py` talks to the Docker daemon to read logs and exec into containers,
`demo_actions.py` sends mail through the demo SMTP server and calls the backend's
admin endpoints, and `e2e_runner.py` orchestrates the synthetic-email test. None of
this is meaningful or safe in production, so the panel ships only with the demo
compose stack and listens on localhost.

## Configuration

`B4IGO_ADMIN_PANEL_PASSWORD`, `B4IGO_ADMIN_PANEL_SECRET`, `B4IGO_ADMIN_TOKEN`,
`B4IGO_BACKEND_URL`, `B4IGO_AI_SERVICE_URL`, `MAIL_HOST`, `MAIL_DOMAIN`,
`MAIL_SMTP_PORT`. See `docs/CONFIGURATION.md`.

## Run

The panel is built and started by `demo/setup.sh` as part of the compose stack. It is
reachable at `http://localhost:5400` with the default password `admin`.
