from flask import *
import requests

app = Flask(__name__)

#TBD
dataURL = "http://localhost:5001"
serviceURL = "http://localhost:5002"

#simple clock non-essential-----------------------
@app.route("/")
def time():
    return f""" 
    <p> A page showing the time </p>

    <p><span id="time"></span></p>
    <script>
        function updatetime(){{
            document.getElementById("time").innerText
            = new Date().toLocaleTimeString();        
            }}
            updatetime();
            setInterval(updatetime, 1000);
    </script>
    """
#Create Client Gateway---------------------------------------
@app.route("/getData/<user_id>", methods=['GET'])
def getData(user_id):

    try:
        response = requests.get(f"{dataURL}/users/{user_id}")
        response.raise_for_status() #exception for bad data
        data1 = response.json()

        fullData = {"userInfo": data1}
        return jsonify(fullData)

    #handle Bad connection
    except requests.exceptions.RequestException as e:
        app.logger.error(f"Error fetching data from service: {e}")
        abort(500, description="communication error")

#End point to send data----------------------------------------
@app.route('/service/<path:subpath>', methods=['GET','POST','PUT','DELETE'])
def proxyToService(subpath):
    url = f"{serviceURL}/{subpath}"

    response = requests.request(
        method=request.method,
        url=url,
        headers=request.headers,
        data=request.get_data(),
        cookies=request.cookies,
        allow_redirects=False
        )

    return Response(
        response.content,
        status = response.status_code,
        headers=dict(response.headers)
        )

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5000)

#TODO
#confirming human in the middle?
#data encryption?
