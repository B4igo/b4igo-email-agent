from flask import *

app = Flask(__name__)

dataRecieved = []

#add recived data to vault
@app.route("/intake", methods=["POST"])
def intake():
    data = request.json
    record = {
        "data": data
        }
    
    dataRecieved.append(record)
    print("vault recieved: ", record)
    return jsonify({"status": "ok"})

#show all vault data
@app.route("/vaultData", methods=["GET"])
def vaultData():
    return jsonify(dataRecieved)

if __name__ == "__main__":
    app.run(debug=True, port=5002)
    