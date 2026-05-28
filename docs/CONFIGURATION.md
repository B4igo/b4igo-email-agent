# Configuration reference

Every service reads its configuration from environment variables. This is the single
source of truth for those variables: the name, its default, the service that reads
it, and what it controls. The demo sets these in `demo/compose.yaml`; production
deployments must supply their own values.

## Variables you must set for production

These have no safe default for a real deployment and must be set deliberately.

| Variable | Read by | What it controls |
|---|---|---|
| `B4IGO_CORS_ORIGINS` | backend | Comma-separated list of browser origins allowed to make credentialed requests. Set to your real frontend origin (and any `chrome-extension://<id>`). A wildcard is not valid with credentials. Default `http://localhost:5173`. |
| `B4IGO_ACCOUNT_MANAGER_TOKEN` | account-manager, backend | Shared internal-service secret sent as `X-Internal-Service-Token`. If unset, account-manager internal endpoints are open. Set the same value on every service that calls account-manager. |
| `B4IGO_ADMIN_TOKEN` | backend, admin-panel | Secret for the backend's demo admin endpoints (`X-Admin-Token`). |
| `B4IGO_API_BASE_URL` | backend (graphql_mapper) | Base URL of the b4igo vault GraphQL gateway. |
| `B4IGO_BACKEND_GRAPHQL_URL` | account-manager | b4igo GraphQL endpoint used by the SIWE auth client. Required at startup. |
| `B4IGO_ACCOUNT_DB_PATH` | account-manager | Path to the linked-account SQLite database. Mount on durable storage; losing it loses every linked account. |
| `OLLAMA_HOST` | ai-service (Ollama client) | URL of the Ollama server hosting the classifier and parser models. |
| `VITE_BACKEND_URL` | frontend (build/runtime) | Backend `/api` base the browser app calls. Default `http://localhost:5000/api`. |

Google OAuth for the Gmail provider is configured through a `client_secrets.json`
file (path overridable via `B4IGO_GOOGLE_CLIENT_SECRETS`, default `client_secrets.json`).
The real file is gitignored; copy `client_secrets.json.example` and fill in your own
Google project's client ID, secret, and the production redirect URIs and JavaScript
origins. The browser extension's allowed hosts live in
`frontend/public/manifest.json` and must be updated to your production domain.

## Service URLs

Inter-service URL defaults point at `localhost` so a single service runs standalone
in development. Compose overrides them with in-network service names.

| Variable | Default | Read by |
|---|---|---|
| `B4IGO_ACCOUNT_MANAGER_URL` | `http://localhost:5100` | backend, scheduler |
| `B4IGO_AI_SERVICE_URL` | `http://localhost:5300` | backend, scheduler |
| `B4IGO_BACKEND_URL` | `http://localhost:5000` | backend (self/redirect base) |
| `B4IGO_FRONTEND_URL` | `http://localhost:5173` | backend (OAuth redirects) |
| `BACKEND_URL` | `http://localhost:5000` | ai-service |
| `B4IGO_ACCOUNT_MANAGER_PUBLIC_URL` | `http://127.0.0.1:5100` | account-manager (OAuth redirect URIs) |
| `B4IGO_SCHEDULER_URL` | (unset) | account-manager (notify on new account) |

## Scheduler

| Variable | Default | Controls |
|---|---|---|
| `REDIS_HOST` | `localhost` | Redis host |
| `REDIS_PORT` | `6379` | Redis port |
| `POLL_INTERVAL_SECONDS` | `10` | How often to poll account-manager. Use 60 to 300 in production to respect provider rate limits. |
| `QUEUE_INTERVAL_SECONDS` | `2` | How often to drain the Redis queue into ai-service. |

## AI service

| Variable | Default | Controls |
|---|---|---|
| `AI_SERVICE_PORT` | `5300` | Listen port |
| `PARSER_MODEL` | unset (`qwen3:8b`) | Ollama model for schema extraction |
| `RERANKER_MODEL` | unset | Cross-encoder model for classification reranking |
| `OLLAMA_HOST` | Ollama default | Ollama server URL |

## Backend

| Variable | Default | Controls |
|---|---|---|
| `B4IGO_VAULT_BACKEND` | `""` | Selects vault storage backend (`api` for the b4igo gateway). |
| `B4IGO_API_KEY` | `""` | Bearer token for the vault API. |
| `B4IGO_API_TIMEOUT_SECS` | `10` | Vault API request timeout. |
| `B4IGO_GRAPHQL_ENDPOINT` | `/graphql` | GraphQL path appended to the API base. |

## Account manager

| Variable | Default | Controls |
|---|---|---|
| `B4IGO_ACCOUNT_MANAGER_PORT` | `5100` | Listen port |
| `B4IGO_GOOGLE_CLIENT_SECRETS` | `client_secrets.json` | Path to Google OAuth client secrets |

## Admin panel (demo only)

| Variable | Default | Controls |
|---|---|---|
| `B4IGO_ADMIN_PANEL_PASSWORD` | `admin` | Login password |
| `B4IGO_ADMIN_PANEL_SECRET` | `""` | Session signing secret |
| `B4IGO_PANEL_CONTAINERS` | `""` | Containers the panel may inspect |
| `MAIL_HOST` | `mailserver` | Demo SMTP host for sending test emails |
| `MAIL_DOMAIN` | `test.local` | Demo mail domain |
| `MAIL_SMTP_PORT` | `25` | Demo SMTP port |

## Testing

| Variable | Default | Controls |
|---|---|---|
| `RUN_OLLAMA_TESTS` | unset | Set to `1` to run the ai_pipeline tests that need a live Ollama server. Off by default so `pytest` and CI skip them. |
| `B4IGO_BACKEND_GRAPHQL_URL` | - | Required to import the account-manager service in its unit tests; any placeholder works since the tests do not call it. |
