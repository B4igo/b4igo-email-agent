# ai-service

Flask service (port 5300) that turns raw email (and attachments) into structured
entries. It classifies the message domain and extracts schema-typed records using a
local Ollama model, then posts each entry to the backend confirmation queue.

## Pipeline

`ai_pipeline/` composes two stages:

1. **DomainClassifier** (`domain_classifier.py`): classifies the text into
   `education`, `health`, `legal`, `personal`, or `other`, using a sentence-transformers
   cross-encoder and Ollama. Low-confidence results are promoted to `other`.
2. **DomainParser** (`domain_parser.py`): for a supported domain, prompts Ollama with
   the domain's Pydantic schemas (`shared/schemas/`) and validates the JSON response
   into model instances.

`AIPipeline.SUPPORTED_DOMAINS` controls which domains are parsed. Documents and
attachments (PDF, DOCX, and similar) are converted to text with docling before
classification.

## Key endpoints

| Method | Path | Purpose |
|---|---|---|
| POST | `/api/ai/text` | Classify and parse a plain-text message |
| POST | `/api/ai/text-with-attachments` | Same, with base64 attachments to convert first |

Each parsed entry is posted to the backend at `/api/confirmations/enqueue`. The admin
panel can call the pipeline in a dry-run mode that returns entries without enqueuing.

## Configuration

`OLLAMA_HOST`, `BACKEND_URL`, `AI_SERVICE_PORT`, and the optional `PARSER_MODEL` /
`RERANKER_MODEL` overrides. The default parser model is `qwen3:8b`. See
`docs/CONFIGURATION.md`.

## Run standalone

```bash
pip install -r ai_service/requirements.txt
# requires a reachable Ollama server with the parser model pulled
python -m ai_service.app
```

## Tests

- `ai_service/tests/test_app.py` covers the HTTP layer with mocks.
- `ai_service/ai_pipeline/tests/` runs accuracy tests against a real Ollama server and
  is gated behind `RUN_OLLAMA_TESTS=1`. These need `sentence-transformers` and a
  running model server, so a normal `pytest` run skips them.
