"""Email agent API for handling authentication and confirmation requests."""

import json
import logging
import os
import sys
from concurrent.futures import ThreadPoolExecutor
from typing import Any
from urllib.parse import urlencode
from uuid import uuid4

from flask import Flask, jsonify, redirect, request
from flask_cors import CORS
from flask_jwt_extended import (
    JWTManager,
    create_access_token,
    create_refresh_token,
    get_jwt_identity,
    jwt_required,
    set_access_cookies,
    set_refresh_cookies,
    unset_jwt_cookies,
)
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
logger = logging.getLogger(__name__)

# FLASK RUNTIME INIT
# set the url to the frontend url provided by npm run dev
app = Flask(__name__)
CORS(app, origins=["http://localhost:5173"], supports_credentials=True)


# configure Flask to handle larger requests and timeouts
app.config["MAX_CONTENT_LENGTH"] = 16 * 1024 * 1024  # 16MB max
# thread pool executor for async operations
executor = ThreadPoolExecutor(max_workers=4)


# AUTHENTICATION INIT

# set the secret key for JWT signing
app.config["JWT_SECRET_KEY"] = str(uuid4())  # TODO: save as file on server
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = 3600  # 1 hour
app.config["JWT_REFRESH_TOKEN_EXPIRES"] = 86400  # 1 day

jwt = JWTManager(app)
account_manager_client = AccountManagerClient()
frontend_base_url = os.environ.get("B4IGO_FRONTEND_URL", "http://localhost:5173").rstrip("/")
backend_base_url = os.environ.get("B4IGO_BACKEND_URL", "http://localhost:5000").rstrip("/")


def _seed_login_users() -> None:
    """Seed local dev login users in account manager auth storage."""
    demo_users = [
        (os.environ.get("B4IGO_DEMO_USERNAME", "user"), os.environ.get("B4IGO_DEMO_PASSWORD", "password"), "user"),
        (
            os.environ.get("B4IGO_ADMIN_USERNAME", "admin"),
            os.environ.get("B4IGO_ADMIN_PASSWORD", "adminpass"),
            "admin",
        ),
    ]

    for username, password, role in demo_users:
        try:
            response = account_manager_client.seed_user(username=username, password=password, role=role)
            if response.status_code >= 400:
                logger.warning("Failed to seed login user %s via account manager", username)
        except RequestException as exc:
            logger.warning("Skipping login seed; account manager unavailable: %s", exc)
            break


_seed_login_users()


# ROUTES


@app.route("/api/health", methods=["GET"])
def health_check():
    """Health check endpoint."""
    return jsonify({"status": "healthy", "service": __name__})


# AUTH
@app.route("/api/auth/login", methods=["POST"])
def login():
    """Authenticate user and return JWT tokens."""
    username = request.json.get("username")
    password = request.json.get(
        "password"
    )  # TODO: align hash methods frontend -> backend

    if not username or not password:
        return jsonify({"error": "Missing username or password"}), 400

    try:
        auth_response = account_manager_client.verify_user(username, password)
    except RequestException as exc:
        logger.error("AccountManager auth verify failed: %s", exc)
        return jsonify({"error": "Authentication service unavailable"}), 503

    if auth_response.status_code == 401:
        return jsonify({"error": "Invalid username or password"}), 401
    if auth_response.status_code >= 400:
        return jsonify({"error": "Failed to authenticate"}), 502

    # generate tokens
    access_token = create_access_token(identity=username)
    refresh_token = create_refresh_token(identity=username)

    # optionally, set cookies
    response = jsonify({"access_token": access_token, "refresh_token": refresh_token})
    set_access_cookies(response, access_token)
    set_refresh_cookies(response, refresh_token)

    return response


# refresh current token
@app.route("/api/auth/refresh", methods=["POST"])
@jwt_required(refresh=True)
def refresh():
    """Refresh access token using refresh token."""
    current_user = get_jwt_identity()
    new_access_token = create_access_token(identity=current_user)
    response = jsonify(access_token=new_access_token)
    set_access_cookies(response, new_access_token)
    return response


# logout of current credentials
@app.route("/api/auth/logout", methods=["POST"])
def logout():
    """Logout current user and clear cookies."""
    response = jsonify({"message": "Logged out"})
    unset_jwt_cookies(response)
    return response


# test if current credentials are valid
@app.route("/api/auth/test-credentials", methods=["GET"])
@jwt_required()
def test_credentials():
    """Test if current credentials are valid."""
    current_user = get_jwt_identity()
    return jsonify(logged_in_as=current_user), 200


# CONFIRMATIONS MANAGEMENT (no auth - for testing integration)
@app.route("/api/confirmations/enqueue", methods=["POST"])
def enqueue_confirmation():
    """Enqueue a confirmation for a specific user."""
    try:
        data = request.get_json()
        if not data or "username" not in data or "jsonPayload" not in data:
            return (
                jsonify({"error": "Missing required fields: username, jsonPayload"}),
                400,
            )

        username = data["username"]
        json_payload = data["jsonPayload"]

        try:
            exists_response = account_manager_client.user_exists(username)
            exists_payload = exists_response.json()
            if exists_response.status_code >= 400 or not exists_payload.get("exists"):
                return jsonify({"error": f"User '{username}' does not exist"}), 404
        except RequestException as exc:
            logger.error("AccountManager user existence check failed: %s", exc)
            return jsonify({"error": "Authentication service unavailable"}), 503
        except ValueError:
            return jsonify({"error": "Invalid response from authentication service"}), 502

        confirmation_id = db.add_confirmation(username, json_payload)
        if confirmation_id:
            logger.info(
                "enqueued confirmation id %s for user %s", confirmation_id, username
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
        logger.error("Error enqueueing confirmation: %s", e)
        return jsonify({"error": "Failed to enqueue confirmation"}), 500


@app.route("/api/confirmations/user/<username>", methods=["GET"])
def get_user_confirmations(username):
    """Get all confirmations for a specific user."""
    confirmations_list = db.get_confirmations(username)

    if confirmations_list:
        return jsonify({"username": username, "confirmations": confirmations_list}), 200

    else:
        return jsonify({"msg": f"No confirmations found for {username}"}), 404


# CONFIRMATIONS (auth required)
@app.route("/api/confirmations", methods=["GET"])
@jwt_required()
def confirmations():
    """Get all pending confirmations for current user."""
    current_user = get_jwt_identity()

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
        current_user = get_jwt_identity()

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

def _background_ai_upload(username: str, files_data: list):
    import requests
    try:
        response = requests.post(
            "http://localhost:5300/api/ai/text-with-attachments",
            data={"username": username, "text": ""},
            files=files_data,
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
    current_user = get_jwt_identity()

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
    current_user = get_jwt_identity()
    try:
        response = account_manager_client.list_accounts(current_user)
        accounts = response.json()
    except RequestException as exc:
        logger.error("AccountManager list call failed: %s", exc)
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
    current_user = get_jwt_identity()
    try:
        response = account_manager_client.delete_account(current_user, connector_id)
    except RequestException as exc:
        logger.error("AccountManager delete call failed: %s", exc)
        return jsonify({"error": "Account manager service unavailable"}), 503

    if response.status_code == 204:
        logger.info("Removed email connector id %s for user %s", connector_id, current_user)
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
        logger.error("AccountManager provider types call failed: %s", exc)
        return jsonify({"error": "Account manager service unavailable"}), 503
    except ValueError:
        return jsonify({"error": "Invalid response from account manager"}), 502


@app.route("/api/email-connectors/setup/<connector_type>", methods=["GET"])
@jwt_required()
def get_connector_setup(connector_type):
    """Get setup steps for a provider and normalize callback URLs for frontend."""
    current_user = get_jwt_identity()
    try:
        response = account_manager_client.get_provider_setup(
            provider=connector_type,
            b4igo_user_id=current_user,
            connector_name=request.args.get("name"),
        )
        if response.status_code >= 400:
            return jsonify(response.json()), response.status_code

        steps = response.json()

        return jsonify(steps), 200

    except Exception as e:
        logger.error("Error getting connector setup for %s: %s", connector_type, e)
        return jsonify({"error": "Failed to get setup steps"}), 500


@app.route("/api/email-connectors/status/<state_id>", methods=["GET"])
@jwt_required()
def get_email_connector_status(state_id: str):
    """Proxy the OAuth status check to the account manager."""
    try:
        response = account_manager_client.session.get(
            f"{account_manager_client.base_url}/api/providers/status/{state_id}",
            headers=account_manager_client._auth_headers(),
            timeout=10,
        )
        return jsonify(response.json()), response.status_code
    except RequestException as exc:
        logger.error("AccountManager status poll failed: %s", exc)
        return jsonify({"error": "Account manager service unavailable"}), 503

@app.route("/api/email-step-callback/<provider>/<function_name>", methods=["POST"])
@jwt_required()
def run_email_step_callback(provider: str, function_name: str):
    """Run one provider setup callback through account manager validation logic."""
    current_user = get_jwt_identity()

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
        logger.error("AccountManager step callback call failed: %s", exc)
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
            return _redirect_with_params({"success": "0", "error": "Missing OAuth code or state"})

        callback_url = f"{backend_base_url}/api/email-connectors/oauth/callback/{provider}"
        response = account_manager_client.complete_provider_oauth(
            provider=provider,
            auth_code=auth_code,
            state=state,
            oauth_callback_url=callback_url,
        )
        result = response.json()
        if response.status_code >= 400:
            logger.warning("Provider OAuth callback failed for %s: %s", provider, result)
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
        logger.error("Error in provider OAuth callback for %s: %s", provider, e)
        return _redirect_with_params({"success": "0", "error": "Failed to complete authorization"})


@app.route("/api/accounts/link", methods=["POST"])
@jwt_required()
def link_account():
    """Link an email provider account for the authenticated user."""
    data = request.get_json(silent=True) or {}
    current_user = get_jwt_identity()
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
        logger.error("AccountManager link call failed: %s", exc)
        return jsonify({"error": "Account manager service unavailable"}), 503
    except ValueError:
        return jsonify({"error": "Invalid response from account manager"}), 502


@app.route("/api/accounts", methods=["GET"])
@jwt_required()
def list_accounts():
    """List linked provider accounts for the authenticated user."""
    current_user = get_jwt_identity()
    try:
        response = account_manager_client.list_accounts(current_user)
        return jsonify(response.json()), response.status_code
    except RequestException as exc:
        logger.error("AccountManager list call failed: %s", exc)
        return jsonify({"error": "Account manager service unavailable"}), 503
    except ValueError:
        return jsonify({"error": "Invalid response from account manager"}), 502


@app.route("/api/accounts/<int:account_id>", methods=["DELETE"])
@jwt_required()
def delete_account(account_id: int):
    """Delete one linked account for the authenticated user."""
    current_user = get_jwt_identity()
    try:
        response = account_manager_client.delete_account(current_user, account_id)
        if response.content:
            return jsonify(response.json()), response.status_code
        return "", response.status_code
    except RequestException as exc:
        logger.error("AccountManager delete call failed: %s", exc)
        return jsonify({"error": "Account manager service unavailable"}), 503
    except ValueError:
        return jsonify({"error": "Invalid response from account manager"}), 502


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
