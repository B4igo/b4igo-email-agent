# backend

Flask API (port 5000) that handles authentication, the confirmation queue, vault
writes, and file uploads. It is the service the frontend talks to directly.

## Responsibilities

- Authentication: proxies SIWE init/verify and JWT validation to account-manager.
- Confirmation queue: stores parsed entries (SQLite via `shared/database.py`) that
  ai-service enqueues, and serves them to the frontend for review.
- Vault writes: on accept, maps the entry to a b4igo GraphQL mutation through
  `shared/graphql_mapper.py` and writes it to the vault, then deletes the
  confirmation. Reject just deletes it.
- File upload: accepts documents and forwards them to ai-service for parsing.
- Email connectors: proxies the account linking and provider setup flows to
  account-manager.

## Key endpoints

| Method | Path | Purpose |
|---|---|---|
| GET | `/api/health` | Liveness check |
| POST | `/api/auth/init`, `/api/auth/verify`, `/api/auth/logout` | SIWE authentication |
| POST | `/api/confirmations/enqueue` | Internal: ai-service adds a parsed entry |
| GET | `/api/confirmations` | List pending confirmations for the user |
| POST | `/api/accept-confirmation`, `/api/reject-confirmation` | Accept (write to vault) or reject |
| POST | `/api/file/upload` | Upload a document for parsing |
| POST | `/api/accounts/link`, GET `/api/accounts` | Linked email accounts |

## Configuration

Reads `B4IGO_CORS_ORIGINS`, `B4IGO_ACCOUNT_MANAGER_URL`, `B4IGO_ACCOUNT_MANAGER_TOKEN`,
`B4IGO_AI_SERVICE_URL`, `B4IGO_FRONTEND_URL`, `B4IGO_BACKEND_URL`, `B4IGO_ADMIN_TOKEN`,
and the vault variables (`B4IGO_API_BASE_URL`, `B4IGO_API_KEY`, `B4IGO_VAULT_BACKEND`).
See `docs/CONFIGURATION.md`.

## Run standalone

```bash
pip install -r backend/requirements.txt
python backend/app.py
```

Run the full stack with `demo/setup.sh` (see the root README).

## Tests

Vault and confirmation logic is covered under `shared/vault/tests/`. Run from the repo
root with `pytest`.
