#!/bin/sh
# Wrapper entrypoint: injects domain config into SnappyMail's data directory,
# then hands off to the original entrypoint.

set -e

DOMAIN_DIR="/var/lib/snappymail/_data_/_default_/domains"

# The original entrypoint initializes the data directory structure on first run.
# We need that to happen first, so we run it briefly in the background, wait for
# the directory to appear, then inject our config.

# If the domains dir doesn't exist yet, start the real entrypoint to init it.
if [ ! -d "$DOMAIN_DIR" ]; then
    echo "[snappymail-init] First run — initializing data directory..."
    # Run the original entrypoint for a few seconds to trigger init
    /entrypoint.sh &
    PID=$!

    # Wait for the directory structure to be created
    for i in $(seq 1 30); do
        if [ -d "$DOMAIN_DIR" ]; then
            break
        fi
        sleep 1
    done

    # Kill the background process — we'll restart it properly below
    kill $PID 2>/dev/null || true
    wait $PID 2>/dev/null || true
    sleep 1
fi

# Inject domain config
if [ -d "$DOMAIN_DIR" ]; then
    echo "[snappymail-init] Installing test.local domain config..."
    cp /snappymail-config/test.local.json "$DOMAIN_DIR/test.local.json"
    chown nobody:nobody "$DOMAIN_DIR/test.local.json" 2>/dev/null || true

    # Remove the default wildcard domain if it exists (so test.local is the only option)
    rm -f "$DOMAIN_DIR/disabled-default.json"
else
    echo "[snappymail-init] WARNING: domains directory not found at $DOMAIN_DIR"
fi

echo "[snappymail-init] Starting SnappyMail..."
exec /entrypoint.sh
