from flask import Flask, request, jsonify

app = Flask(__name__)

myval = 0

@app.route("/", methods=["GET"])
def get_value():
    return jsonify(myval)

@app.route("/", methods=["POST"])
def set_value():
    global myval
    myval = request.form["v"]
    return jsonify(myval)

@app.route("/", methods=["PUT"])
def reset_value():
    global myval
    myval = 100
    return jsonify(myval)

app.run(debug=True, port=4999)