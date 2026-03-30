#!/usr/bin/env bash
# Generate config/postfix-accounts.cf from seed/accounts.json, then start compose.
# Usage: ./setup.sh [docker compose args...]
#   e.g. ./setup.sh up -d
#        ./setup.sh down -v   (to wipe everything)

set -euo pipefail
cd "$(dirname "$0")"

# Generate accounts config from the JSON source of truth
python3 -c "
import json
accounts = json.load(open('seed/accounts.json'))
for a in accounts:
    print(f\"{a['email']}|{{PLAIN}}{a['password']}\")
" > config/postfix-accounts.cf

echo "Generated config/postfix-accounts.cf with $(wc -l < config/postfix-accounts.cf) accounts"

# Tear down old volumes for a fresh start
docker compose down -v 2>/dev/null || true

docker compose "${@:-up}"
