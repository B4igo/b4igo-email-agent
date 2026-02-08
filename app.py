"""Email agent API for handling authentication and confirmation requests."""

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
# example users for the moment (will be sqlite db)
users = {
    "user": {"password": "password", "role": "user"},
    "admin": {"password": "adminpass", "role": "admin"},
}

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

    user = users.get(username)
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


# CONFIRMATIONS


@app.route("/api/confirmations", methods=["GET"])
@jwt_required()
def confirmations():
    """Get all pending confirmations for current user."""
    current_user = get_jwt_identity()

    # TODO: replace dict with sqlite in-memory
    confirmations = {
        "user": [
            {"id": 3, "jsonPayload": '{"example_key2" : "example_value2"}'},
            {"id": 4, "jsonPayload": '{"example_key3" : "example_value3"}'},
        ],
        "admin": [
            {"id": 0, "jsonPayload": '{"example_key" : "example_value"}'},
            {"id": 1, "jsonPayload": '{"example_key1" : "example_value1"}'},
        ],
    }

    if current_user in confirmations.keys():
        return jsonify(confirmations[current_user]), 200

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
        logger.info("removing id %s", id)  # TODO: stubbed DB call

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

        id = data["id"]

        if "jsonPayload" in data:
            logger.info("using provided jsonPayload")

        # here we would grab either the paylod from the db or use
        # the jsonPayload edit provided.
        logger.info(
            "adding confirmation #%s to valut", id
        )  # TODO: stubbed B4iGo API call

        return "", 200

    except Exception:
        return jsonify({"error": "Missing 'id' parameter"}), 400


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
