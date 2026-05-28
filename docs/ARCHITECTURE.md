# Architecture

The b4igo-email-agent is a pipeline of small services that pull a user's inbound
email, classify and parse each message with a local LLM, and queue structured
entries for the user to confirm into the b4igo vault. Each service is independently
containerized and communicates over HTTP, with Redis for queueing and an external
GraphQL gateway for vault writes.

## High-level flow

```
mailserver --> account-manager --> scheduler --> ai-service --> backend --> frontend
              (IMAP/Gmail pull)  (Redis queue)  (classify,     (confirm    (review and
                                                  parse)         queue)      accept)
```

1. The **scheduler** polls **account-manager** on a fixed interval for each
   registered account.
2. **account-manager** calls the account's provider (IMAP or Gmail), returns any
   unseen messages, and marks them seen so later polls skip them.
3. The **scheduler** pushes each message onto a Redis queue and forwards it to
   **ai-service**, retrying on failure and parking exhausted jobs in a dead-letter
   queue.
4. **ai-service** classifies the message domain and, for a supported domain,
   extracts structured entries, posting each to the **backend** confirmation queue.
5. The user opens the **frontend**, reviews pending confirmations, and accepts or
   rejects each. Accepted entries are written to the b4igo vault through the
   backend.

## Services

| Service | Dir | Port | Framework | Responsibility |
|---|---|---|---|---|
| account-manager | `account_manager/` | 5100 | Flask | Linked-account records, SIWE auth, provider pull logic (IMAP, Gmail OAuth) |
| scheduler | `scheduler/` | 5200 | Flask + APScheduler | Periodic polling, Redis queueing, AI handoff, retries, dead-letter |
| ai-service | `ai_service/` | 5300 | Flask | Domain classification and schema extraction via Ollama; attachment to text |
| backend | `backend/` | 5000 | Flask | Auth, confirmation queue (SQLite), vault writes via GraphQL, file upload |
| frontend | `frontend/` | 5173 | React + Vite | User UI for linking accounts and confirming entries; browser extension build |
| admin-panel | `admin_panel/` | 5400 | FastAPI | Demo-only operations UI (logs, demo emails, end-to-end test). Not for production |
| redis | (image) | 6379 | - | Queues for the scheduler |
| mailserver / webmail | (image) | 1025/1143/8888 | - | Demo mail only; replaced by the user's real provider in production |

Service directories use underscores. Docker Compose service names and container
names use hyphens (DNS convention), so the inter-service URLs reference hosts like
`http://account-manager:5100`.

## Service-to-service contracts

- **scheduler to account-manager**: `POST /api/pull` with `{b4igoUserId, accountIds}`
  returns unseen messages. Account enrollment is `POST /api/scheduler/registry`.
- **scheduler to ai-service**: `POST /api/ai/text` and
  `POST /api/ai/text-with-attachments` with the message text, originating user, and
  decoded attachments.
- **ai-service to backend**: `POST /api/confirmations/enqueue` with
  `{user_id, jsonPayload, schemaName}` for each parsed entry.
- **backend to account-manager**: the backend proxies auth and account endpoints to
  account-manager through `shared/account_manager/client.py`.
- **backend to b4igo vault**: on accept, `shared/graphql_mapper.py` maps the parsed
  schema to a GraphQL mutation against the external gateway. Unknown schemas fall
  back to a generic note (`createNotesInput`).

### Internal service token

Calls to account-manager's internal endpoints and the backend's demo admin endpoint
are gated by shared secrets passed as request headers:

- `B4IGO_ACCOUNT_MANAGER_TOKEN` -> `X-Internal-Service-Token` (service to service).
- `B4IGO_ADMIN_TOKEN` -> `X-Admin-Token` (admin panel to backend demo endpoints).

If `B4IGO_ACCOUNT_MANAGER_TOKEN` is unset the internal endpoints are open, which is
acceptable only on a trusted network (the demo leaves it unset).

## The shared package

`shared/` is imported by the services as a top-level package. Key modules:

| Module | Purpose | Used by |
|---|---|---|
| `shared/database.py` | SQLite confirmation store | backend |
| `shared/graphql_mapper.py` | Maps parsed schemas to b4igo vault GraphQL mutations | backend |
| `shared/account_manager/` | Account linking, SIWE auth, providers (IMAP, Gmail) | account-manager, backend (client only) |
| `shared/vault/` | Vault client with pluggable storage (SQLite or b4igo API) | backend, tests |
| `shared/schemas/` | Pydantic models per domain (health, legal, personal, education) and the LLM prompt builder | ai-service, tests |
| `shared/mail/` | Email input models and parsing helpers | ai-service |

## Domains and parsing

`ai_service/ai_pipeline/domain_classifier.py` classifies a message into one of
`education`, `health`, `legal`, `personal`, or `other`. For every domain except
`other`, `domain_parser.py` extracts structured entries using the Pydantic models in
`shared/schemas/`. The set of parseable domains is `AIPipeline.SUPPORTED_DOMAINS`.

See `docs/CONFIGURATION.md` for every environment variable and
`docs/integration/` for the vault and confirmation API references.
