# Roadmap and known limitations

This collects the open work and known gaps in the codebase so none of them read as
silent omissions. These are not blockers for the handoff; they are the next things a
maintaining team would pick up.

## Production hardening

- **WSGI server.** The backend, account-manager, scheduler, and ai-service run the
  Flask development server (the Dockerfiles run `python app.py`). Put a production
  WSGI runner (gunicorn or uvicorn) in front of each before exposing them outside a
  trusted network.
- **Account database durability.** account-manager stores linked accounts in SQLite.
  The demo does not mount a volume. In production, mount `B4IGO_ACCOUNT_DB_PATH` onto
  durable storage.
- **Internal service token.** Set `B4IGO_ACCOUNT_MANAGER_TOKEN` so internal endpoints
  are not open. See `docs/CONFIGURATION.md`.
- **OAuth and extension origins.** Update `client_secrets.json` redirect URIs and
  `frontend/public/manifest.json` host permissions to your production domain.

## Functional gaps (existing TODOs in code)

- `ai_service/ai_pipeline/ai_pipeline.py`: validate input size against the model's
  max token window (batch or truncate oversized documents).
- `ai_service/app.py`: the allowed file-extension set and the docling converter
  configuration need review for the full range of supported document types.
- `backend/app.py`: error handling when forwarding a confirmation to the ai-service
  is incomplete; failures are not caught and surfaced.
- `shared/schemas/schema_prompter.py`: prompt strings are rebuilt on every call and
  could be cached.
- `frontend/src/Functions/Helpers.ts`: the polling loop could back off when there is
  no change or no user interaction.

## Education domain

The classifier and parser support an `education` domain, but the b4igo vault has no
dedicated education record type, so accepted education entries are stored through the
generic note mutation (`createNotesInput`). Add a typed mapping in
`shared/graphql_mapper.py` if the vault gains an education type.

## Test coverage

Unit tests cover the vault, account-manager, and schema-prompter logic with mocks and
run in CI. The ai_pipeline accuracy tests require a live Ollama server and are gated
behind `RUN_OLLAMA_TESTS`. There is no automated coverage yet for the scheduler, the
backend HTTP endpoints, the admin panel, or the frontend.
