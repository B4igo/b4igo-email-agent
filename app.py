"""Email agent API for handling authentication and confirmation requests."""

import json
import logging
import sys
from concurrent.futures import ThreadPoolExecutor
from uuid import uuid4

from flask import Flask, jsonify, request
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

from b4igo_email_agent.database import db
from b4igo_email_agent.vault.client import VaultClient
from b4igo_email_agent.vault.utils import parse_vault_record
from b4igo_email_agent.email_connectors.gmail_connector import (
    get_authorization_url,
    handle_oauth_callback,
    get_user_email_from_token,
)
from b4igo_email_agent.email_connectors.connector_types import ConnectorType

# Store for PKCE code verifiers keyed by OAuth state
_oauth_code_verifiers: dict[str, str] = {}

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
# Initialize database with example users
db.add_user("user", "password", "user")
db.add_user("admin", "adminpass", "admin")
db.add_confirmation("user", '{"example_key2" : "example_value2"}')
db.add_confirmation("user", '{"example_key3" : "example_value3"}')
db.add_confirmation("admin", '{"example_key" : "example_value"}')
db.add_confirmation("admin", '{"example_key1" : "example_value1"}')

# set the secret key for JWT signing
app.config["JWT_SECRET_KEY"] = str(uuid4())  # TODO: save as file on server
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = 3600  # 1 hour
app.config["JWT_REFRESH_TOKEN_EXPIRES"] = 86400  # 1 day

jwt = JWTManager(app)


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

    user = db.get_user(username)
    if not user or user["password"] != password:
        return jsonify({"error": "Invalid username or password"}), 401

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

        if not db.get_user(username):
            return jsonify({"error": f"User '{username}' does not exist"}), 404

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

@app.route("/api/email-connectors", methods=["GET"])
@jwt_required()
def get_email_connectors():
    """Get all email connectors for the current user."""
    current_user = get_jwt_identity()

    connectors = db.get_email_connectors(current_user)

    for connector in connectors:
        connector["has_token"] = bool(connector.get("token_json"))
        connector.pop("token_json", None)

    return jsonify(connectors), 200


@app.route("/api/email-connectors/<int:connector_id>", methods=["DELETE"])
@jwt_required()
def remove_email_connector(connector_id):
    """Remove an email connector by ID."""
    current_user = get_jwt_identity()

    if db.remove_email_connector(connector_id, current_user):
        logger.info("Removed email connector id %s for user %s", connector_id, current_user)
        return jsonify({"message": "Email connector removed successfully"}), 200
    else:
        return jsonify({"error": "Connector not found or does not belong to user"}), 404


@app.route("/api/email-connectors/types", methods=["GET"])
@jwt_required()
def get_connector_type_options():
    """Get list of available connector types (e.g., ['gmail'])."""
    connector_types = [t.value for t in ConnectorType]
    return jsonify(connector_types), 200


@app.route("/api/email-connectors/setup/<connector_type>", methods=["GET"])
@jwt_required()
def get_connector_setup(connector_type):
    """Get the setup steps required for a specific connector type."""
    try:
        if connector_type == ConnectorType.GMAIL.value:
            redirect_uri = "http://localhost:5173/email-connectors/gmail/callback"
            client_secrets_file = "client_secrets.json"
            
            auth_url, state, code_verifier = get_authorization_url(client_secrets_file, redirect_uri)

            _oauth_code_verifiers[state] = code_verifier

            steps = [
                {
                    "type": "redirect",
                    "title": "Authorize Gmail Access",
                    "desc": "You will be redirected to Google to authorize access to your Gmail account",
                    "callback": "/api/email-connectors/gmail/callback",
                    "value": auth_url,
                    "state": state
                }
            ]
            
            return jsonify(steps), 200
        else:
            return jsonify({"error": f"Unsupported connector type: {connector_type}"}), 400

    except Exception as e:
        logger.error("Error getting connector setup for %s: %s", connector_type, e)
        return jsonify({"error": "Failed to get setup steps"}), 500


@app.route("/api/email-connectors/gmail/callback", methods=["GET"])
@jwt_required()
def gmail_oauth_callback():
    """Handle OAuth callback from Gmail authorization."""
    try:
        current_user = get_jwt_identity()
        
        auth_code = request.args.get("code")
        state = request.args.get("state")
        
        if not auth_code:
            return jsonify({"error": "Missing authorization code"}), 400
        
        connector_name = request.args.get("name", "Gmail Account")
        
        redirect_uri = "http://localhost:5173/email-connectors/gmail/callback"
        client_secrets_file = "client_secrets.json"
        
        code_verifier = _oauth_code_verifiers.pop(state, None) if state else None

        token_json = handle_oauth_callback(auth_code, client_secrets_file, redirect_uri, state, code_verifier)

        connector_email = get_user_email_from_token(token_json)
        
        if db.email_already_connected(current_user, connector_email):
            logger.warning(
                "User %s attempted to connect already connected email %s",
                current_user,
                connector_email
            )
            return jsonify({
                "error": f"Email {connector_email} is already connected to your account"
            }), 409
        
        connector_id = db.add_email_connector(
            username=current_user,
            connector_type=ConnectorType.GMAIL.value,
            connector_name=connector_name,
            token_json=token_json,
            connector_email=connector_email
        )
        
        if connector_id:
            logger.info(
                "Successfully added Gmail connector id %s for user %s (email: %s)",
                connector_id,
                current_user,
                connector_email
            )
            return jsonify({
                "message": "Gmail account connected successfully",
                "id": connector_id,
                "connector_email": connector_email
            }), 201
        else:
            logger.error("Failed to add Gmail connector for user %s", current_user)
            return jsonify({"error": "Failed to save email connector"}), 500
        
    except Exception as e:
        logger.error("Error in Gmail OAuth callback for user %s: %s", get_jwt_identity(), e)
        return jsonify({"error": f"Failed to complete authorization: {str(e)}"}), 500


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
