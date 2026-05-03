"""Smoke test: exercises add_record + delete_record for all four record types
against the live B4iGO dev API via B4igoVaultApiStorage.

Usage:
    B4IGO_API_BASE_URL=https://gatewayservice-test-684919379591.us-central1.run.app \
    B4IGO_API_KEY=<jwt> \
    B4IGO_GRAPHQL_ENDPOINT=/query \
    B4IGO_TEST_USER_ID=<uuid> \
    python test_query.py

Set DEBUG=1 to print raw API responses for failed calls.
"""

import os
import sys

sys.path.insert(0, os.path.dirname(__file__))

USER_ID = os.environ.get("B4IGO_TEST_USER_ID", "")
if not USER_ID:
    sys.exit("ERROR: set B4IGO_TEST_USER_ID to your user UUID")
if not os.environ.get("B4IGO_API_KEY"):
    sys.exit("ERROR: set B4IGO_API_KEY to your JWT token")
if not os.environ.get("B4IGO_API_BASE_URL"):
    sys.exit(
        "ERROR: set B4IGO_API_BASE_URL"
        " (e.g. https://gatewayservice-test-684919379591.us-central1.run.app)"
    )

import requests  # noqa: E402

from shared.vault.b4igo_api_storage import B4igoVaultApiStorage  # noqa: E402

DEBUG = os.environ.get("DEBUG", "").strip() == "1"


class _DebugSession(requests.Session):
    """Thin wrapper that prints raw responses when DEBUG=1."""

    def post(self, url, **kwargs):
        resp = super().post(url, **kwargs)
        if DEBUG:
            try:
                import json

                print(f"    [debug] {resp.status_code} {url}")
                print(f"    [debug] {json.dumps(resp.json(), indent=6)}")
            except Exception:
                print(f"    [debug] {resp.status_code} {resp.text[:300]}")
        return resp


session = _DebugSession()
session.headers.update(
    {
        "Authorization": f"Bearer {os.environ['B4IGO_API_KEY']}",
        "Content-Type": "application/json",
    }
)

storage = B4igoVaultApiStorage(session=session)

TEST_CASES = [
    (
        "doctor",
        {"doctor_name": "Smoke Test Doctor", "location": "555-0000"},
    ),
    (
        "insurance",
        {"type_of_health_insurance": "PPO Smoke Test"},
    ),
    (
        "medication",
        {"name_of_medicine": "Smoke Test Med", "side_effect": "None"},
    ),
    (
        "medical_history",
        {"disease": "Smoke Test Condition", "description": "Integration test"},
    ),
]

passed = 0
failed = 0

for record_type, payload in TEST_CASES:
    print(f"\n{'─' * 50}")
    print(f"  {record_type}")

    record_id = storage.add_record(USER_ID, record_type, payload)
    if record_id is None:
        print(f"  FAIL  add_record returned None  (run with DEBUG=1 for details)")
        failed += 1
        continue
    print(f"  PASS  add_record  -> id={record_id}")

    deleted = storage.delete_record(record_id, record_type=record_type, username=USER_ID)
    if deleted:
        print(f"  PASS  delete_record id={record_id}")
    else:
        print(f"  WARN  delete_record returned False — record may remain in DB")

    passed += 1

print(f"\n{'─' * 50}")
print(f"  {passed} passed, {failed} failed")
if failed:
    sys.exit(1)
