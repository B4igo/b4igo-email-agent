#!/usr/bin/env bash
# Demo launcher for B4iGO Email Agent
#
# Generates the mail server accounts config, then starts the full stack.
#
# Usage:
#   ./setup.sh           # foreground
#   ./setup.sh -d        # detached
#   ./setup.sh down -v   # tear down and wipe volumes

set -euo pipefail
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
SMTP_TEST_DIR="$SCRIPT_DIR/smtp-imap-test"
ACCOUNTS_FILE="$SMTP_TEST_DIR/seed/accounts.json"
CONFIG_DIR="$SMTP_TEST_DIR/config"

# ── Generate postfix-accounts.cf from accounts.json ──
echo "Generating mail accounts config..."
mkdir -p "$CONFIG_DIR"
python3 -c "
import json, sys
with open('$ACCOUNTS_FILE') as f:
    accounts = json.load(f)
lines = [f\"{a['email']}|{{PLAIN}}{a['password']}\" for a in accounts]
print('\n'.join(lines))
" > "$CONFIG_DIR/postfix-accounts.cf"

echo "  → wrote $(wc -l < "$CONFIG_DIR/postfix-accounts.cf") accounts to postfix-accounts.cf"

# ── Verify host Ollama is running with qwen3:8b ──
if ! curl -sf http://localhost:11434/api/tags >/dev/null 2>&1; then
    echo "ERROR: Ollama is not running on the host. Start it with: ollama serve" >&2
    exit 1
fi
if ! curl -sf http://localhost:11434/api/tags | grep -q "qwen3"; then
    echo "ERROR: qwen3:8b model not found. Pull it with: ollama pull qwen3:8b" >&2
    exit 1
fi
echo "  ✓ Host Ollama ready with qwen3:8b"

# ── Tear down previous run (clean volumes for fresh state) ──
echo "Cleaning up previous containers..."
docker compose -f "$SCRIPT_DIR/compose.yaml" down -v 2>/dev/null || true

# ── Start the stack ──
echo ""
echo "Starting B4iGO demo stack..."
echo "  Frontend:  http://localhost:5173  (user / password)"
echo "  Webmail:   http://localhost:8888  (alice@test.local / password123)"
echo "  Backend:   http://localhost:5000/api/health"
echo ""
echo "Note: First run will pull Docker images which may take a few minutes."
echo "      Ollama + qwen3:8b must be running on the host (verified above)."
echo ""

docker compose -f "$SCRIPT_DIR/compose.yaml" up --build "$@"
