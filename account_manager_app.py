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


@app.route("/api/auth/seed-user", methods=["POST"])
def seed_user():
    """Create or update one user for app-level authentication."""
    auth_error = _validate_internal_auth()
    if auth_error:
        return auth_error

    payload: dict[str, Any] = request.get_json(silent=True) or {}
    username = payload.get("username")
    password = payload.get("password")
    role = payload.get("role", "user")
    if not username or not password:
        return jsonify({"error": "Missing required fields: username, password"}), 400

    user = service.seed_user(username=str(username), password=str(password), role=str(role))
    return jsonify(user), 201


@app.route("/api/auth/verify", methods=["POST"])
def verify_user_auth():
    """Validate username/password and return user profile."""
    auth_error = _validate_internal_auth()
    if auth_error:
        return auth_error

    payload: dict[str, Any] = request.get_json(silent=True) or {}
    username = payload.get("username")
    password = payload.get("password")
    if not username or not password:
        return jsonify({"error": "Missing required fields: username, password"}), 400

    user = service.authenticate_user(str(username), str(password))
    if user is None:
        return jsonify({"error": "Invalid username or password"}), 401
    return jsonify(user), 200


@app.route("/api/auth/users/<username>/exists", methods=["GET"])
def user_exists(username: str):
    """Check whether username exists in account-manager auth storage."""
    auth_error = _validate_internal_auth()
    if auth_error:
        return auth_error

    return jsonify({"exists": service.user_exists(username)}), 200


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


@app.route("/api/providers/types", methods=["GET"])
def list_provider_types():
    """List provider types available for generic setup UI."""
    auth_error = _validate_internal_auth()
    if auth_error:
        return auth_error

    return jsonify(service.list_provider_types()), 200


@app.route("/api/providers/<provider>/setup", methods=["POST"])
def get_provider_setup(provider: str):
    """Build provider setup steps including OAuth redirects when required."""
    auth_error = _validate_internal_auth()
    if auth_error:
        return auth_error

    payload: dict[str, Any] = request.get_json(silent=True) or {}
    b4igo_user_id = payload.get("b4igoUserId")
    callback_url = payload.get("oauthCallbackUrl")
    connector_name = payload.get("connectorName")
    if not b4igo_user_id or not callback_url:
        return jsonify({"error": "Missing required fields: b4igoUserId, oauthCallbackUrl"}), 400

    client_secrets_file = os.environ.get("B4IGO_GOOGLE_CLIENT_SECRETS", "client_secrets.json")

    steps = service.get_provider_setup_steps(
        provider=provider,
        b4igo_user_id=b4igo_user_id,
        oauth_callback_url=callback_url,
        client_secrets_file=client_secrets_file,
        connector_name=connector_name,
    )
    if steps is None:
        return jsonify({"error": "Unsupported provider"}), 400
    return jsonify(steps), 200


@app.route("/api/providers/<provider>/steps/<function_name>", methods=["POST"])
def run_provider_step_callback(provider: str, function_name: str):
    """Run one provider callback after validating step count and step types."""
    auth_error = _validate_internal_auth()
    if auth_error:
        return auth_error

    payload: dict[str, Any] = request.get_json(silent=True) or {}
    steps = payload.get("steps")
    b4igo_user_id = payload.get("b4igoUserId")

    if not isinstance(steps, list):
        return jsonify({"error": "Validation error"}), 400

    result = service.run_provider_setup_callback(provider, function_name, steps, b4igo_user_id)
    status = 200 if result.get("success") else 400
    return jsonify(result), status


@app.route("/api/providers/<provider>/oauth/callback", methods=["POST"])
def complete_provider_oauth(provider: str):
    """Complete provider OAuth callback and upsert linked account."""
    auth_error = _validate_internal_auth()
    if auth_error:
        return auth_error

    payload: dict[str, Any] = request.get_json(silent=True) or {}
    auth_code = payload.get("code")
    state = payload.get("state")
    callback_url = payload.get("oauthCallbackUrl")
    if not auth_code or not state or not callback_url:
        return jsonify({"error": "Missing required fields: code, state, oauthCallbackUrl"}), 400

    client_secrets_file = os.environ.get("B4IGO_GOOGLE_CLIENT_SECRETS", "client_secrets.json")

    try:
        account = service.complete_provider_oauth(
            provider=provider,
            auth_code=auth_code,
            state=state,
            client_secrets_file=client_secrets_file,
            redirect_uri=callback_url,
        )
    except Exception as exc:
        logger.error("Failed to complete provider OAuth: %s", exc)
        return jsonify({"error": "Failed to complete authorization"}), 500

    if account is None:
        return jsonify({"error": "Validation error"}), 400
    return jsonify(account), 201


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
