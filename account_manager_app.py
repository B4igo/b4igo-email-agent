"""Standalone Flask microservice for account linking and provider pull."""

import logging
import os
import sys
from typing import Any

from flask import Flask, jsonify, request

from b4igo_email_agent.account_manager.service import AccountManagerService

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)],
)
logger = logging.getLogger(__name__)

app = Flask(__name__)
service = AccountManagerService()


@app.route("/api/health", methods=["GET"])
def health_check():
    """Health check endpoint for account manager service."""
    return jsonify({"status": "healthy", "service": "account_manager"}), 200


@app.route("/api/accounts/link", methods=["POST"])
def link_account():
    """Link or update one provider account for a B4iGO user."""
    auth_error = _validate_internal_auth()
    if auth_error:
        return auth_error

    payload = request.get_json(silent=True) or {}
    required_fields = ["b4igoUserId", "provider", "emailAddress", "credentials"]
    if any(field not in payload for field in required_fields):
        return (
            jsonify(
                {
                    "error": "Missing required fields: "
                    "b4igoUserId, provider, emailAddress, credentials"
                }
            ),
            400,
        )

    provider = payload["provider"]
    if provider not in ("imap", "gmail"):
        return jsonify({"error": "Unsupported provider. Use 'imap' or 'gmail'"}), 400

    account = service.link_account(
        b4igo_user_id=payload["b4igoUserId"],
        provider=provider,
        email_address=payload["emailAddress"],
        credentials=payload["credentials"],
        display_name=payload.get("displayName"),
        config=payload.get("config"),
    )
    if account is None:
        return jsonify({"error": "Invalid credentials/config payload"}), 400

    return jsonify(account), 201


@app.route("/api/accounts/<b4igo_user_id>", methods=["GET"])
def list_accounts(b4igo_user_id: str):
    """List linked accounts for one B4iGO user."""
    auth_error = _validate_internal_auth()
    if auth_error:
        return auth_error

    return jsonify(service.list_accounts(b4igo_user_id)), 200


@app.route("/api/accounts/<b4igo_user_id>/<int:account_id>", methods=["DELETE"])
def delete_account(b4igo_user_id: str, account_id: int):
    """Delete one linked account for one B4iGO user."""
    auth_error = _validate_internal_auth()
    if auth_error:
        return auth_error

    if service.delete_account(b4igo_user_id, account_id):
        return "", 204
    return jsonify({"error": "Account not found"}), 404


@app.route("/api/pull", methods=["POST"])
def pull_accounts():
    """Pull emails for all or selected linked accounts of one user."""
    auth_error = _validate_internal_auth()
    if auth_error:
        return auth_error

    payload: dict[str, Any] = request.get_json(silent=True) or {}
    b4igo_user_id = payload.get("b4igoUserId")
    if not b4igo_user_id:
        return jsonify({"error": "Missing required field: b4igoUserId"}), 400

    account_ids_raw = payload.get("accountIds", [])
    if not isinstance(account_ids_raw, list):
        return jsonify({"error": "accountIds must be a list of integers"}), 400

    try:
        account_ids = [int(account_id) for account_id in account_ids_raw]
    except (TypeError, ValueError):
        return jsonify({"error": "accountIds must be a list of integers"}), 400

    return jsonify(service.pull(b4igo_user_id, account_ids)), 200


def _validate_internal_auth():
    """Validate internal token if configured.

    Returns:
        Flask response tuple on auth error, else None.
    """
    expected = os.environ.get("B4IGO_ACCOUNT_MANAGER_TOKEN")
    if not expected:
        return None

    provided = request.headers.get("X-Internal-Service-Token")
    if provided != expected:
        return jsonify({"error": "Unauthorized"}), 401
    return None


if __name__ == "__main__":
    port = int(os.environ.get("B4IGO_ACCOUNT_MANAGER_PORT", "5100"))
    app.run(debug=True, host="0.0.0.0", port=port)
