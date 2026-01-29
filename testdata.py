from flask import *
import requests

app = Flask(__name__)

serviceURL = "http://localhost:5002"

#create dummy data to send
users = {
    "1": {"id": 1, "name": "John"},
    "2": {"id": 2, "name": "Jane"}
}

#see user data
@app.route("/users/<user_id>", methods=["GET"])
def getUser(user_id):
    if user_id not in users:
        abort(404,"user not found")
    return jsonify(users[user_id])

#send user data to vault
@app.route("/users/<user_id>/send", methods=["POST"])
def sendUser(user_id):
    if user_id not in users:
        abort(404,"user not found")
    
    userdata = users[user_id]

    response = requests.post(f"{serviceURL}/intake", json=userdata)

    return jsonify({"response ": response.json()})

if __name__ == "__main__":
    app.run(debug=True, port=5001)