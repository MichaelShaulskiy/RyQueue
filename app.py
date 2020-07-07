from flask import Flask, request, jsonify, render_template

app = Flask(__name__)


@app.route("/api/<channel>", methods=["GET"])
def get_user(channel):
    pass

@app.route("/api", methods=["POST"])
def add_video():
    pass

@app.route("/")
def index():
    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)