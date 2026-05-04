#!/bin/sh
# Demo bootstrap: link the demo IMAP mailbox to the demo b4igo user, then
# register that account with the scheduler so polling begins.
#
# This stands in for what a real user would do via the frontend "Link account"
# flow. Idempotent: link is upsert and scheduler registry is a Redis set, so
# re-running is safe.
set -eu

ACCOUNT_MANAGER_URL=${ACCOUNT_MANAGER_URL:-http://account-manager:5100}
SCHEDULER_URL=${SCHEDULER_URL:-http://scheduler:5200}
DEMO_USER=${DEMO_USER:-user}
IMAP_EMAIL=${IMAP_EMAIL:-alice@test.local}
IMAP_PASSWORD=${IMAP_PASSWORD:-password123}
IMAP_HOST=${IMAP_HOST:-mailserver}
IMAP_PORT=${IMAP_PORT:-143}

LINK_BODY=$(jq -n \
  --arg user "$DEMO_USER" \
  --arg email "$IMAP_EMAIL" \
  --arg pass "$IMAP_PASSWORD" \
  --arg host "$IMAP_HOST" \
  --argjson port "$IMAP_PORT" '{
    b4igoUserId: $user,
    provider: "imap",
    emailAddress: $email,
    credentials: { username: $email, password: $pass },
    displayName: "Demo IMAP mailbox",
    config: { host: $host, port: $port, use_ssl: false, mailbox: "INBOX" }
  }')

echo "bootstrap: linking $IMAP_EMAIL as IMAP for user '$DEMO_USER'"
ATTEMPT=0
until ACC=$(curl -sf -X POST -H "Content-Type: application/json" \
              -d "$LINK_BODY" "$ACCOUNT_MANAGER_URL/api/accounts/link"); do
  ATTEMPT=$((ATTEMPT + 1))
  if [ "$ATTEMPT" -gt 30 ]; then
    echo "bootstrap: account-manager unreachable after 30 attempts; aborting" >&2
    exit 1
  fi
  echo "bootstrap: account-manager not ready (attempt $ATTEMPT), retrying"
  sleep 3
done

ACC_ID=$(echo "$ACC" | jq -r '.id')
if [ -z "$ACC_ID" ] || [ "$ACC_ID" = "null" ]; then
  echo "bootstrap: link returned no account id; response was: $ACC" >&2
  exit 1
fi
echo "bootstrap: linked as account id $ACC_ID"

REG_BODY=$(jq -n --arg user "$DEMO_USER" --argjson aid "$ACC_ID" \
  '{b4igoUserId: $user, accountId: $aid}')

echo "bootstrap: registering account $ACC_ID with scheduler"
ATTEMPT=0
until curl -sf -X POST -H "Content-Type: application/json" \
        -d "$REG_BODY" "$SCHEDULER_URL/api/scheduler/registry" >/dev/null; do
  ATTEMPT=$((ATTEMPT + 1))
  if [ "$ATTEMPT" -gt 30 ]; then
    echo "bootstrap: scheduler unreachable after 30 attempts; aborting" >&2
    exit 1
  fi
  echo "bootstrap: scheduler not ready (attempt $ATTEMPT), retrying"
  sleep 3
done

echo "bootstrap: complete — account $ACC_ID registered for polling"
