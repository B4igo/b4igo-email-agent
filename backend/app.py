"""Email agent API for handling authentication and confirmation requests."""

import json
import logging
import os
import sys
from concurrent.futures import ThreadPoolExecutor
from functools import wraps
from typing import Any
from urllib.parse import urlencode
from uuid import uuid4

import flask
from flask import Flask, jsonify, redirect, request
from flask_cors import CORS
from requests import RequestException

from shared.account_manager.client import AccountManagerClient
from shared.database import db
from shared.vault.client import VaultClient
from shared.vault.utils import parse_vault_record

from werkzeug.utils import secure_filename

# TODO look through all these and make sure this is for all/most text documents
ALLOWED_FILE_EXTENSIONS = {'txt', 'pdf', 'md', 'docx'}

# LOGGING
# configure logging (does not show in production
# gunicorn server due to threded web-workers).
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)],
)
logger = logging.getLogger("backend")

# FLASK RUNTIME INIT
# set the url to the frontend url provided by npm run dev
app = Flask(__name__)
CORS(app, origins=["chrome-extension://dbpcogloagbfglggnnedldhjfhbpdeof"], supports_credentials=True)


# configure Flask to handle larger requests and timeouts
app.config["MAX_CONTENT_LENGTH"] = 16 * 1024 * 1024  # 16MB max
# thread pool executor for async operations
executor = ThreadPoolExecutor(max_workers=4)


# AUTHENTICATION INIT

account_manager_client = AccountManagerClient()
frontend_base_url = os.environ.get(
    "B4IGO_FRONTEND_URL", "http://localhost:5173"
).rstrip("/")
backend_base_url = os.environ.get("B4IGO_BACKEND_URL", "http://localhost:5000").rstrip(
    "/"
)

AI_SERVICE_URL = os.environ.get("B4IGO_AI_SERVICE_URL", "http://localhost:5300").rstrip("/")

def jwt_required():
    def wrapper(fn):
        @wraps(fn)
        def decorator(*args, **kwargs):
            # Reduced logging for demo
            # logger.info("Authenticating request for %s", request.path)
            auth_header = request.headers.get("Authorization")
            if not auth_header:
                return jsonify({"error": "Missing Authorization header"}), 401

            try:
                response = account_manager_client.auth_validate(auth_header)
                if response.status_code == 200:
                    data = response.json()
                    if data.get("valid") and data.get("userId"):
                        flask.g.current_user = data["userId"]
                        return fn(*args, **kwargs)
            except Exception as e:
                logger.error("Token validation failed: %s", e)

            return jsonify({"error": "Invalid or expired token"}), 401
        return decorator
    return wrapper


# ROUTES


@app.route("/api/health", methods=["GET"])
def health_check():
    """Health check endpoint."""
    return jsonify({"status": "healthy", "service": __name__})


# AUTH
@app.route("/api/auth/init", methods=["POST"])
def auth_init():
    """Initialize SIWE flow."""
    # Reduced logging
    # logger.info("Received request for /api/auth/init")
    payload = request.get_json(silent=True) or {}
    address = payload.get("address")
    if not address:
        return jsonify({"error": "Missing required field: address"}), 400

    try:
        response = account_manager_client.auth_init(address)
        return jsonify(response.json()), response.status_code
    except RequestException as exc:
        return jsonify({"error": "Authentication service unavailable"}), 503

@app.route("/api/auth/verify", methods=["POST"])
def auth_verify():
    """Verify SIWE signature and return JWT."""
    # Reduced logging
    # logger.info("Received request for /api/auth/verify")
    payload = request.get_json(silent=True) or {}
    signature = payload.get("signature")
    request_id = payload.get("requestId")

    if not signature or not request_id:
        return jsonify({"error": "Missing signature or request_id"}), 400

    try:
        response = account_manager_client.auth_verify(signature, request_id)
        return jsonify(response.json()), response.status_code
    except RequestException as exc:
        logger.error("AccountManager auth verify failed: %s", exc)
        return jsonify({"error": "Authentication service unavailable"}), 503

@app.route("/api/auth/logout", methods=["POST"])
def logout():
    """Frontend handles JWT clearing. Return a 200, this will remain for any future changes to the auth flow."""
    return jsonify({"message": "Logged out"}), 200


@app.route("/api/auth/test-credentials", methods=["GET"])
@jwt_required()
def test_credentials():
    """Test if current credentials are valid."""
    current_user = flask.g.current_user
    return jsonify(logged_in_as=current_user), 200


# ADMIN (token-gated, demo only)
@app.route("/api/confirmations/admin/clear", methods=["DELETE"])
def admin_clear_confirmations():
    """Bulk-clear confirmations. Demo-only, gated on B4IGO_ADMIN_TOKEN.

    If the env var is unset, the route is disabled to avoid an unauthenticated
    destructive endpoint in any deployed environment. Optional ?username=<name>
    query param scopes the wipe to a single user.
    """
    expected = os.environ.get("B4IGO_ADMIN_TOKEN")
    if not expected:
        return jsonify({"error": "Admin endpoint disabled"}), 503

    provided = request.headers.get("X-Admin-Token")
    if provided != expected:
        return jsonify({"error": "Forbidden"}), 403

    username = request.args.get("username")
    deleted = db.clear_confirmations(username)
    logger.info(
        "admin clear: removed %s confirmation(s)%s",
        deleted,
        f" for {username}" if username else "",
    )
    return jsonify({"deleted": deleted}), 200


# CONFIRMATIONS MANAGEMENT (no auth - for testing integration)
@app.route("/api/confirmations/enqueue", methods=["POST"])
def enqueue_confirmation():
    """Enqueue a confirmation for a specific user."""
    try:
        data = request.get_json()
        if not data or "user_id" not in data or "jsonPayload" not in data:
            return (
                jsonify({"error": "Missing required fields: user_id, jsonPayload"}),
                400,
            )

        user_id = data["user_id"]
        json_payload = data["jsonPayload"]

        try:
            exists_response = account_manager_client.user_exists(user_id)
            exists_payload = exists_response.json()
            if exists_response.status_code >= 400 or not exists_payload.get("exists"):
                return jsonify({"error": f"User '{user_id}' does not exist"}), 404
        except RequestException as exc:
            logger.error("account manager user existence check failed: %s", exc)
            return jsonify({"error": "Authentication service unavailable"}), 503
        except ValueError:
            return (
                jsonify({"error": "Invalid response from authentication service"}),
                502,
            )

        confirmation_id = db.add_confirmation(user_id, json_payload)
        if confirmation_id:
            logger.info(
                "enqueued confirmation id %s for user %s", confirmation_id, user_id
            )
            return (
                jsonify(
                    {
                        "message": "Confirmation enqueued successfully",
                        "id": confirmation_id,
                    }
                ),
                201,
            )

        else:
            return jsonify({"error": "Failed to enqueue confirmation"}), 500

    except Exception as e:
        logger.error("error enqueueing confirmation: %s", e)
        return jsonify({"error": "Failed to enqueue confirmation"}), 500


@app.route("/api/confirmations/user/<user_id>", methods=["GET"])
def get_user_confirmations(user_id):
    """Get all confirmations for a specific user."""
    confirmations_list = db.get_confirmations(user_id)

    if confirmations_list:
        return jsonify({"user_id": user_id, "confirmations": confirmations_list}), 200

    else:
        return jsonify({"msg": f"No confirmations found for {user_id}"}), 404


# CONFIRMATIONS (auth required)
@app.route("/api/confirmations", methods=["GET"])
@jwt_required()
def confirmations():
    """Get all pending confirmations for current user."""
    current_user = flask.g.current_user

    confirmations_list = db.get_confirmations(current_user)

    if confirmations_list:
        return jsonify(confirmations_list), 200

    else:
        return jsonify({"msg": f"No confirmations found for {current_user}"})


@app.route("/api/reject-confirmation", methods=["POST"])
@jwt_required()
def reject_confirmation():
    """Reject a confirmation by ID."""
    try:
        data = request.get_json()
        if not data or "id" not in data:
            raise Exception("missing id parameter")

        id = data["id"]
        if db.remove_confirmation(id):
            logger.info("removed confirmation id %s", id)
        else:
            logger.info("confirmation id %s not found", id)

        return "", 200

    except Exception:
        return jsonify({"error": "Missing 'id' parameter"}), 400


# handles both blanket accept and edits
@app.route("/api/accept-confirmation", methods=["POST"])
@jwt_required()
def accept_confirmation():
    """Accept a confirmation by ID, optionally with edited payload."""
    try:
        data = request.get_json()
        if not data or "id" not in data:
            raise Exception("missing id parameter")

        conf_id = data["id"]
        current_user = flask.g.current_user

        if not db.confirmation_exists(conf_id):
            return jsonify({"error": "Confirmation not found"}), 404

        # Use edited payload if provided, else load from DB
        if "jsonPayload" in data:
            logger.info("using provided jsonPayload")
            raw = data["jsonPayload"]
        else:
            confirmations_list = db.get_confirmations(current_user)
            conf = next((c for c in confirmations_list if c["id"] == conf_id), None)
            if not conf:
                return jsonify({"error": "Confirmation not found"}), 404
            raw = conf["jsonPayload"]

        # Normalize to dict if string
        if isinstance(raw, str):
            try:
                payload = json.loads(raw)
            except json.JSONDecodeError:
                db.remove_confirmation(conf_id)
                return jsonify({"error": "Invalid jsonPayload"}), 400
        else:
            payload = raw if isinstance(raw, dict) else {}

        record = parse_vault_record(payload)
        if record:
            vault = VaultClient()
            vault_id = vault.create(current_user, record)
            if vault_id is None:
                logger.warning("vault create failed for confirmation #%s", conf_id)
                return jsonify({"error": "Vault write failed"}), 502
            logger.info(
                "added confirmation #%s to vault as record id %s", conf_id, vault_id
            )
        else:
            logger.warning(
                "could not parse vault record from confirmation #%s", conf_id
            )

        db.remove_confirmation(conf_id)
        return "", 200

    except Exception:
        return jsonify({"error": "Missing 'id' parameter"}), 400

@app.route("/api/file/types", methods=["GET"])
def get_file_types():
    """Get allowed file types for upload."""
    return jsonify({"allowed_file_types": list(ALLOWED_FILE_EXTENSIONS)}), 200

def _background_ai_upload(user_id: str, files_data: list):
    import requests
    try:
        # Include internal service token
        headers = {}
        service_token = os.environ.get("B4IGO_ACCOUNT_MANAGER_TOKEN")
        if service_token:
            headers["X-Internal-Service-Token"] = service_token

        response = requests.post(
            f"{AI_SERVICE_URL}/api/ai/text-with-attachments",
            data={"username": user_id, "text": ""},
            files=files_data,
            headers=headers,
            timeout=30
        )
        if response.status_code not in (200, 201, 202):
            logger.error("Failed to send files to AI pipeline: %s", response.text)
    except Exception as e:
        logger.error("Error calling AI pipeline: %s", e)

@app.route("/api/file/upload", methods=["POST"])
@jwt_required()
def upload_files():
    """Accept multiple files, check file types, and get the authenticated user."""
    current_user = flask.g.current_user

    def allowed_file(filename):
        return '.' in filename and \
            filename.rsplit('.', 1)[1].lower() in ALLOWED_FILE_EXTENSIONS

    if 'files' not in request.files:
        return jsonify({"error": "No 'files' found in the request."}), 400

    files = request.files.getlist('files')

    if not files or files[0].filename == '':
        return jsonify({"error": "No files selected."}), 400

    accepted_files = []
    rejected_files = []

    for file in files:
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            accepted_files.append(filename)
        else:
            rejected_files.append(file.filename)

    if len(rejected_files) > 0:
        return jsonify({"error": "Invalid file type(s)", "rejected_files": rejected_files}), 400
    else:
        files_payload = []
        for file in files:
            file.seek(0)
            files_payload.append(('files', (file.filename, file.read(), file.mimetype)))

        #TODO: need to catch errors sending to the ai service.
        executor.submit(_background_ai_upload, current_user, files_payload)

        return jsonify({
            "message": "Files processed",
            "username": current_user,
            "accepted_files": accepted_files,
            "rejected_files": rejected_files
        }), 200


@app.route("/api/email-connectors", methods=["GET"])
@jwt_required()
def get_email_connectors():
    """Get all email connectors for the current user."""
    current_user = flask.g.current_user
    try:
        response = account_manager_client.list_accounts(current_user)
        accounts = response.json()
    except RequestException as exc:
        logger.error("account manager list call failed: %s", exc)
        return jsonify({"error": "Account manager service unavailable"}), 503
    except ValueError:
        return jsonify({"error": "Invalid response from account manager"}), 502

    connectors = [
        {
            "id": account["id"],
            "connector_type": account["provider"],
            "connector_name": account.get("displayName") or account["emailAddress"],
            "connector_email": account["emailAddress"],
            "has_token": bool(account.get("credentials")),
            "last_read": None,
            "last_error_msg": None,
        }
        for account in accounts
    ]

    return jsonify(connectors), 200


@app.route("/api/email-connectors/<int:connector_id>", methods=["DELETE"])
@jwt_required()
def remove_email_connector(connector_id):
    """Remove an email connector by ID."""
    current_user = flask.g.current_user
    try:
        response = account_manager_client.delete_account(current_user, connector_id)
    except RequestException as exc:
        logger.error("account manager delete call failed: %s", exc)
        return jsonify({"error": "Account manager service unavailable"}), 503

    if response.status_code == 204:
        logger.info(
            "removed email connector id %s for user %s", connector_id, current_user
        )
        return jsonify({"message": "Email connector removed successfully"}), 200
    if response.status_code == 404:
        return jsonify({"error": "Connector not found or does not belong to user"}), 404
    return jsonify({"error": "Failed to remove connector"}), 502


@app.route("/api/email-connectors/types", methods=["GET"])
@jwt_required()
def get_connector_type_options():
    """Get list of available connector types from account manager."""
    try:
        response = account_manager_client.list_provider_types()
        return jsonify(response.json()), response.status_code
    except RequestException as exc:
        logger.error("account manager provider types call failed: %s", exc)
        return jsonify({"error": "Account manager service unavailable"}), 503
    except ValueError:
        return jsonify({"error": "Invalid response from account manager"}), 502


@app.route("/api/email-connectors/setup/<connector_type>", methods=["GET"])
@jwt_required()
def get_connector_setup(connector_type):
    """Get setup steps for a provider and normalize callback URLs for frontend."""
    current_user = flask.g.current_user
    try:
        callback_url = f"{backend_base_url}/api/email-connectors/oauth/callback/{connector_type}"
        response = account_manager_client.get_provider_setup(
            provider=connector_type,
            b4igo_user_id=current_user,
            connector_name=request.args.get("name"),
            oauth_callback_url=callback_url,
        )
        if response.status_code >= 400:
            return jsonify(response.json()), response.status_code

        steps = response.json()

        return jsonify(steps), 200

    except Exception as e:
        logger.error("error getting connector setup for %s: %s", connector_type, e)
        return jsonify({"error": "Failed to get setup steps"}), 500


@app.route("/api/email-connectors/status/<state_id>", methods=["GET"])
@jwt_required()
def get_email_connector_status(state_id: str):
    """Proxy the OAuth status check to the account manager."""
    try:
        response = account_manager_client.check_oauth_status(state_id)
        return jsonify(response.json()), response.status_code
    except RequestException as exc:
        logger.error("account manager status poll failed: %s", exc)
        return jsonify({"error": "Account manager service unavailable"}), 503


@app.route("/api/email-step-callback/<provider>/<function_name>", methods=["POST"])
@jwt_required()
def run_email_step_callback(provider: str, function_name: str):
    """Run one provider setup callback through account manager validation logic."""
    current_user = flask.g.current_user

    payload: dict[str, Any] = request.get_json(silent=True) or {}
    steps = payload.get("steps")
    if not isinstance(steps, list):
        return jsonify({"error": "Validation error"}), 400

    try:
        response = account_manager_client.run_provider_step_callback(
            provider=provider,
            function_name=function_name,
            steps=steps,
            b4igo_user_id=current_user,
        )
        return jsonify(response.json()), response.status_code
    except RequestException as exc:
        logger.error("account manager step callback call failed: %s", exc)
        return jsonify({"error": "Account manager service unavailable"}), 503
    except ValueError:
        return jsonify({"error": "Invalid response from account manager"}), 502


@app.route("/api/email-connectors/oauth/callback/<provider>", methods=["GET"])
def provider_oauth_callback(provider: str):
    """Handle provider OAuth callback and redirect to generic frontend callback page."""
    frontend_callback_url = f"{frontend_base_url}/email-connectors/callback"

    def _redirect_with_params(params: dict[str, str]) -> Any:
        return redirect(f"{frontend_callback_url}?{urlencode(params)}")

    try:
        auth_code = request.args.get("code")
        state = request.args.get("state")
        if not auth_code or not state:
            return _redirect_with_params(
                {"success": "0", "error": "Missing OAuth code or state"}
            )

        callback_url = (
            f"{backend_base_url}/api/email-connectors/oauth/callback/{provider}"
        )
        response = account_manager_client.complete_provider_oauth(
            provider=provider,
            auth_code=auth_code,
            state=state,
            oauth_callback_url=callback_url,
        )
        result = response.json()
        if response.status_code >= 400:
            logger.warning(
                "provider oauth callback failed for %s: %s", provider, result
            )
            return _redirect_with_params(
                {
                    "success": "0",
                    "error": str(result.get("error", "OAuth callback failed")),
                }
            )

        connector_email = str(result.get("emailAddress", ""))
        return _redirect_with_params(
            {
                "success": "1",
                "email": connector_email,
                "id": str(result.get("id", "")),
            }
        )
    except Exception as e:
        logger.error("error in provider oauth callback for %s: %s", provider, e)
        return _redirect_with_params(
            {"success": "0", "error": "Failed to complete authorization"}
        )


@app.route("/api/accounts/link", methods=["POST"])
@jwt_required()
def link_account():
    """Link an email provider account for the authenticated user."""
    data = request.get_json(silent=True) or {}
    current_user = flask.g.current_user
    b4igo_user_id = data.get("b4igoUserId", current_user)

    required_fields = ["provider", "emailAddress", "credentials"]
    if any(field not in data for field in required_fields):
        return (
            jsonify(
                {
                    "error": (
                        "Missing required fields: provider, emailAddress, credentials"
                    )
                }
            ),
            400,
        )

    try:
        response = account_manager_client.link_account(
            b4igo_user_id=b4igo_user_id,
            provider=data["provider"],
            email_address=data["emailAddress"],
            credentials=data["credentials"],
            display_name=data.get("displayName"),
            config=data.get("config"),
        )
        return jsonify(response.json()), response.status_code
    except RequestException as exc:
        logger.error("account manager link call failed: %s", exc)
        return jsonify({"error": "Account manager service unavailable"}), 503
    except ValueError:
        return jsonify({"error": "Invalid response from account manager"}), 502


@app.route("/api/accounts", methods=["GET"])
@jwt_required()
def list_accounts():
    """List linked provider accounts for the authenticated user."""
    current_user = flask.g.current_user
    try:
        response = account_manager_client.list_accounts(current_user)
        return jsonify(response.json()), response.status_code
    except RequestException as exc:
        logger.error("account manager list call failed: %s", exc)
        return jsonify({"error": "Account manager service unavailable"}), 503
    except ValueError:
        return jsonify({"error": "Invalid response from account manager"}), 502


@app.route("/api/accounts/<int:account_id>", methods=["DELETE"])
@jwt_required()
def delete_account(account_id: int):
    """Delete one linked account for the authenticated user."""
    current_user = flask.g.current_user
    try:
        response = account_manager_client.delete_account(current_user, account_id)
        if response.content:
            return jsonify(response.json()), response.status_code
        return "", response.status_code
    except RequestException as exc:
        logger.error("account manager delete call failed: %s", exc)
        return jsonify({"error": "Account manager service unavailable"}), 503
    except ValueError:
        return jsonify({"error": "Invalid response from account manager"}), 502


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
