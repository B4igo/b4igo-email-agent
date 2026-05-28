# b4igo-email-agent

A pipeline that pulls inbound email from a user's linked accounts, classifies
and parses each message via a local LLM, then enqueues structured entries for
the user to confirm in the b4igo vault.

## Architecture

```
mailserver → account-manager (IMAP/Gmail pull) → scheduler (Redis queue)
            → ai-service (classify, parse) → backend (confirmation queue) → frontend
```

Components:

- **mailserver / webmail**: docker-mailserver + SnappyMail. In production the
  user's own provider (Gmail, generic IMAP) replaces this.
- **account-manager** (port 5100): owns linked-account records and provider
  pull logic. Exposes `POST /api/accounts/link` and `POST /api/pull`.
- **redis** (port 6379): queues for the scheduler.
- **scheduler** (port 5200): periodic worker that calls
  `account-manager /api/pull` for each registered account and forwards new
  emails to ai-service. Tracks in-flight jobs and a dead-letter queue.
- **ai-service** (port 5300): classifies the email's domain (health, legal,
  personal) and extracts structured entries via Ollama (qwen3:8b by default).
  Posts each entry to the backend's confirmation queue.
- **backend** (port 5000): authentication, confirmation queue, vault writes
  on user accept.
- **frontend** (port 5173): React/Vite app where the user reviews
  confirmations and links email accounts.
- **admin-panel** (port 5400, demo only): operations UI for inspecting
  containers, sending test emails, and running an end-to-end pipeline check.

## Documentation

- [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md): services, the end-to-end pipeline,
  the shared package, and service-to-service contracts.
- [docs/CONFIGURATION.md](docs/CONFIGURATION.md): every environment variable, its
  default, and which values must change for production.
- [docs/ROADMAP.md](docs/ROADMAP.md): known limitations and open work.
- Per-service notes live in each service's `README.md` (`backend/`, `ai_service/`,
  `scheduler/`, `account_manager/`, `admin_panel/`, `frontend/`).
- [docs/integration/](docs/integration/): vault and confirmation API references.
  `docs/integration/API.md` is an imported copy of B4iGO's own gateway API reference
  and is kept verbatim.

## Running the demo

The demo packages the full stack as a single `docker compose` setup. Useful
for local development and for showing the pipeline working without setting up
real OAuth or real mail accounts.

Prerequisites:

1. Docker and `docker compose`.
2. Ollama running on the host with `qwen3:8b` pulled. `ollama serve` then
   `ollama pull qwen3:8b`. The setup script verifies this.

Start the stack from the repo root:

```bash
cd demo
./setup.sh -d
```

`setup.sh` rebuilds images each run (`--build`), generates `postfix-accounts.cf`
from the seed account list, and brings up nine containers. The `bootstrap`
container runs once and exits. It links `alice@test.local` as an IMAP account
under the `user` b4igo identity and registers it with the scheduler so polling
starts.

Endpoints:

- Frontend: http://localhost:5173 (login `user` / `password`)
- Webmail: http://localhost:8888 (login `alice@test.local` / `password123`)
- Backend health: http://localhost:5000/api/health
- Admin panel: http://localhost:5400 (default password `admin`, bound to
  127.0.0.1)

Mailboxes start empty. Drive activity from the admin panel:

- *Demo Actions*: send canned scenarios or custom emails to any seed account.
- *E2E Test*: drop one synthetic email and watch each pipeline stage flip
  green based on its container's live log stream. Useful as a smoke test
  whenever a service changes.
- *Pipeline Trace*: combined live log stream from each pipeline stage.
- *AI Playground*: feed arbitrary text through the AI pipeline in dry-run
  mode, see the parsed entries without enqueuing.

Tear down:

```bash
docker compose -f demo/compose.yaml down -v
```

`-v` drops the maildata volume and the account-manager SQLite, so the next
`setup.sh` starts from scratch.

## Running in production

Production runs the same components as the demo with three differences:

1. No `bootstrap` container. Real users link their own accounts via the
   frontend, which goes through `account-manager`'s OAuth or IMAP setup
   flows. The frontend (or backend on successful link) calls
   `POST /api/scheduler/registry` to enroll the account for polling.
2. No `mailserver` or `webmail`. Mail comes from the user's own provider.
3. Ollama runs as its own container with the parser/reranker models
   preloaded, instead of on the developer's host.

Per-component requirements:

| Service          | Port | Required configuration                                                                              |
|------------------|------|-----------------------------------------------------------------------------------------------------|
| account-manager  | 5100 | `B4IGO_ACCOUNT_DB_PATH`, `B4IGO_ACCOUNT_MANAGER_TOKEN`, `B4IGO_BACKEND_GRAPHQL_URL`                 |
| redis            | 6379 | none                                                                                                |
| scheduler        | 5200 | `REDIS_HOST`, `REDIS_PORT`, `B4IGO_ACCOUNT_MANAGER_URL`, `B4IGO_AI_SERVICE_URL`, `POLL_INTERVAL_SECONDS` |
| ai-service       | 5300 | `OLLAMA_HOST`, `BACKEND_URL`, optional `PARSER_MODEL`, `RERANKER_MODEL`                             |
| backend          | 5000 | `B4IGO_ACCOUNT_MANAGER_URL`, `B4IGO_ACCOUNT_MANAGER_TOKEN`, `B4IGO_FRONTEND_URL`, `B4IGO_CORS_ORIGINS`, `B4IGO_API_BASE_URL` |
| frontend         | 5173 | `VITE_BACKEND_URL` pointing at the backend `/api`                                                   |

Every environment variable, its default, and which service reads it is documented in
[docs/CONFIGURATION.md](docs/CONFIGURATION.md).

Choices that matter:

- Set `B4IGO_CORS_ORIGINS` (comma-separated) to the frontend origin the browser
  app is served from, plus any `chrome-extension://<id>` origin if the extension
  calls the backend. It defaults to `http://localhost:5173` for the demo. A
  wildcard origin is not valid for credentialed requests, so the backend will not
  accept browser calls from an origin that is not listed.
- Update the Google OAuth `client_secrets.json` redirect URIs and the browser
  extension hosts in `frontend/public/manifest.json` to your production domain.
  The real `client_secrets.json` is gitignored; start from
  `client_secrets.json.example`.
- Set `B4IGO_ACCOUNT_MANAGER_TOKEN` so internal calls share a secret. Without
  it, the internal endpoints on account-manager are open. The same token must
  be present on every service that calls account-manager.
- Persist `account-manager`'s SQLite. The demo does not mount a volume; in
  production mount `/app/email_agent.db` (or whatever
  `B4IGO_ACCOUNT_DB_PATH` points at) onto durable storage. Losing the DB
  loses every linked account.
- Set `POLL_INTERVAL_SECONDS` to something longer than the demo's 5 seconds.
  60 to 300 seconds is reasonable for real IMAP and Gmail providers without
  hitting rate limits.
- Run Ollama with the model preloaded so the first request after a deploy
  does not time out. The demo bumps the scheduler's request timeout to 300s
  for the same reason.
- Replace the Flask development server in front of `backend`,
  `account-manager`, `scheduler`, and `ai-service` with a production WSGI
  runner (gunicorn, uvicorn) before exposing any of them outside trusted
  networks. The current Dockerfiles run the dev server.

The runtime flow once a user has linked an account:

1. `scheduler` polls `account-manager /api/pull` on the configured interval.
2. `account-manager` calls the registered provider (IMAP, Gmail) and returns
   any unseen messages, marking them seen so subsequent polls skip them.
3. `scheduler` queues each email in Redis (`mail_pull_queue`) and processes
   one at a time, posting it to `ai-service /api/ai/text` with the
   originating user as `username`.
4. `ai-service` classifies the email's domain. If the domain has a parser
   (health, legal, personal today), it extracts structured entries and posts
   each one to `backend /api/confirmations/enqueue`. Other domains return an
   empty result.
5. The user opens the frontend and accepts or rejects each pending
   confirmation, which writes the accepted entry into the b4igo vault.

## Setup

### Backend
Install the requirements (it's recommended to create a pyenv or conda environment first).
 ```bash
   pip install -r backend/requirements.txt
   ```
Install the git hooks:
   ```bash
   pre-commit install
   ```

### AccountManager microservice (internal)
Run the dedicated account manager server separately from the backend:
```bash
pip install -r account_manager/requirements.txt
python3 account_manager/account_manager_app.py
```

Optional environment variables:
- `B4IGO_ACCOUNT_MANAGER_PORT` (default `5100`)
- `B4IGO_ACCOUNT_DB_PATH` (default `email_agent.db`)
- `B4IGO_ACCOUNT_MANAGER_TOKEN` (if set, required in header `X-Internal-Service-Token`)

The backend (`backend/app.py`) calls this internal service through `B4IGO_ACCOUNT_MANAGER_URL` (default `http://127.0.0.1:5100`).

### Frontend
Open the terminal in the `frontend` folder and run npm install
to install the frontend packages (assuming that npm is already installed)
```bash
   npm i
```

Then use npm run dev to run the frontend:
```bash
   npm run dev
```

To run the frontend as an extension:
1. Open a terminal in `frontend` and build the app:
   ```bash
   npm run build
   ```
2. Open your Chromium-based browser (Chrome, Edge, etc.) and go to `chrome://extensions/` (or `edge://extensions/`). 
3. Turn on Developer mode in the top right corner. 
4. Click Load unpacked. 
5. Select the `frontend/dist` folder.


## Testing

Run the test suite from the repo root:

```bash
pytest
```

The ML-free unit tests under `shared/` run anywhere. The `ai_service/ai_pipeline`
accuracy tests drive a real local Ollama server and are skipped unless you set
`RUN_OLLAMA_TESTS=1`. CI runs the ML-free suites on every push and pull request to
`main`. See [docs/Tests.md](docs/Tests.md) and [docs/ROADMAP.md](docs/ROADMAP.md) for
coverage gaps.

## Using commit hooks

Once installed, the hooks will run automatically on `git commit`. If any hook fails, the commit will be blocked.

### Manual execution

Run hooks on all files:
```bash
pre-commit run --all-files
```

Run hooks on staged files only:
```bash
pre-commit run
```

Run a specific hook:
```bash
pre-commit run black --all-files
```

### Skipping hooks (not recommended)

If you need to commit without running hooks:
```bash
git commit --no-verify
```

This can be done to save/share work without needing to pass the commit
hooks. They will need to be passed eventually.
