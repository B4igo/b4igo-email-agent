# account-manager

Flask service (port 5100) that owns linked-account records and the provider pull
logic. It is an internal service: the backend and scheduler call it, the frontend
does not call it directly.

## Responsibilities

- Authentication: SIWE init/verify and JWT validation against the b4igo GraphQL
  gateway.
- Linked accounts: stores email account records (IMAP credentials or Gmail OAuth
  tokens) in SQLite and exposes link, list, and delete operations.
- Provider setup: drives the multi-step setup flows for each provider, including the
  Google OAuth callback.
- Pulling mail: `POST /api/pull` calls the registered provider (IMAP via `imaplib`,
  Gmail via the API), returns unseen messages with attachments, and marks them seen.

The business logic lives in the `shared/account_manager/` package; this directory
holds the Flask entrypoint.

## Key endpoints

| Method | Path | Purpose |
|---|---|---|
| GET | `/api/health` | Liveness check |
| POST | `/api/auth/init`, `/api/auth/verify`, GET `/api/auth/validate` | SIWE auth |
| POST | `/api/accounts/link`, GET `/api/accounts/<user>` | Linked accounts |
| GET/POST | `/api/providers/...` | Provider setup and OAuth callback |
| POST | `/api/pull` | Return unseen messages for the given accounts |

Internal endpoints are gated by `X-Internal-Service-Token` when
`B4IGO_ACCOUNT_MANAGER_TOKEN` is set.

## Configuration

`B4IGO_ACCOUNT_MANAGER_PORT`, `B4IGO_ACCOUNT_DB_PATH`, `B4IGO_ACCOUNT_MANAGER_TOKEN`,
`B4IGO_BACKEND_GRAPHQL_URL`, `B4IGO_ACCOUNT_MANAGER_PUBLIC_URL`, `B4IGO_SCHEDULER_URL`,
and `B4IGO_GOOGLE_CLIENT_SECRETS`. See `docs/CONFIGURATION.md`. The real
`client_secrets.json` is gitignored; start from `client_secrets.json.example`.

## Run standalone

```bash
pip install -r account_manager/requirements.txt
B4IGO_BACKEND_GRAPHQL_URL=<gateway-url> python account_manager/account_manager_app.py
```

## Tests

`shared/account_manager/tests/` covers the service and storage with fake providers.
Run from the repo root with `pytest`.
