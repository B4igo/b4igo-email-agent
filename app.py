from flask import Flask, jsonify, request
from flask_jwt_extended import (
    JWTManager, create_access_token, create_refresh_token,
    jwt_required, get_jwt_identity, set_access_cookies,
    set_refresh_cookies, unset_jwt_cookies
)
from uuid import uuid4

# ---- [LOGGING] ----
# configure logging (does not show in production
# gunicorn server due to threded web-workers).
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)],
)
logger = logging.getLogger(__name__)

# ---- [FLASK RUNTIME INIT] ----
app = Flask(__name__)
CORS(app)


# configure Flask to handle larger requests and timeouts
app.config["MAX_CONTENT_LENGTH"] = 16 * 1024 * 1024  # 16MB max
# thread pool executor for async operations
executor = ThreadPoolExecutor(max_workers=4)


# ---- [AUTHENTICATION INIT] ----
# example users for the moment (will be sqlite db)
users = {
    "user": {"password": "password", "role": "user"},
    "admin": {"password": "adminpass", "role": "admin"}
}

# set the secret key for JWT signing
app.config['JWT_SECRET_KEY'] = str(uuid4())  # TODO: save as file on server
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = 3600  # 1 hour
app.config['JWT_REFRESH_TOKEN_EXPIRES'] = 86400  # 1 day

jwt = JWTManager(app)


## ------ [ROUTES] ------

@app.route("/api/health", methods=["GET"])
def health_check():
    """Health check endpoint"""
    return jsonify({"status": "healthy", "service": __name__})

# ---- [AUTH] ----
@app.route('/api/auth/login', methods=['POST'])
def login():
    username = request.json.get('username')
    password = request.json.get('password') # TODO: align hash methods frontend -> backend

    if not username or not password:
        return jsonify({"error": "Missing username or password"}), 400

    user = users.get(username)
    if not user or user['password'] != password:
        return jsonify({"error": "Invalid username or password"}), 401

    # generate tokens
    access_token = create_access_token(identity=username)
    refresh_token = create_refresh_token(identity=username)

    # optionally, set cookies
    response = jsonify({
        'access_token': access_token,
        'refresh_token': refresh_token
    })
    set_access_cookies(response, access_token)
    set_refresh_cookies(response, refresh_token)

    return response


# refresh current token
@app.route('/api/auth/refresh', methods=['POST'])
@jwt_required(refresh=True)
def refresh():
    current_user = get_jwt_identity()
    new_access_token = create_access_token(identity=current_user)
    response = jsonify(access_token=new_access_token)
    set_access_cookies(response, new_access_token)
    return response

# logout of current credentials
@app.route('/api/auth/logout', methods=['POST'])
def logout():
    response = jsonify({"message": "Logged out"})
    unset_jwt_cookies(response)
    return response

# test if current credentials are valid
@app.route('/api/auth/test-credentials', methods=['GET'])
@jwt_required()
def protected():
    current_user = get_jwt_identity()
    return jsonify(logged_in_as=current_user), 200

# ---- [CONFIRMATIONS] ----

@app.route('/api/confirmations', methods=['GET'])
@jwt_required()
def protected():
    current_user = get_jwt_identity()

    # TODO: replace dict with sqlite in-memory
    confirmations = {
        'user' : [
            {
                'id': 3,
                'json-payload' : '{"example_key2" : "example_value2"}'
            },
            {
                'id' : 4,
                'json-payload' : '{"example_key3" : "example_value3"}'
            }
        ],
        'admin' : [
            {
                'id': 0,
                'json-payload' : '{"example_key" : "example_value"}'
            },
            {
                'id' : 1,
                'json-payload' : '{"example_key1" : "example_value1"}'
            }
        ]
    }

    if current_user in confirmations.keys():
        return jsonify(confirmations[current_user]), 200
    
    else:
        return jsonify({'msg' : f'No confirmations found for {current_user}'})


@app.route('/api/reject-confirmation', methods=['POST'])
@jwt_required()
def protected():
    try:
        data = request.get_json()
        if not data or "id" not in data:
            raise Exception('missing id parameter')

        id = data['id']
        logger.info('removing id %s', id) #TODO: stubbed DB call

        return 200
    
    except:
        return jsonify({'error' : "Missing 'id' parameter"}), 400

# handles both blanket accept and edits
@app.route('/api/accept-confirmation', methods=['POST'])
@jwt_required()
def protected():
    try:
        data = request.get_json()
        if not data or "id" not in data:
            raise Exception('missing id parameter')

        id = data['id']

        if "json-payload" in data:
            payload = data['json-payload']

        # here we would grab either the paylod from the db or use 
        # the json-payload edit provided.
        logger.info('adding confirmation #%s to valut', id) #TODO: stubbed B4iGo API call

        return 200
    
    except:
        return jsonify({'error' : "Missing 'id' parameter"}), 400