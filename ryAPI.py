from flask import Flask, render_template, request
from flask_restful import Resource, Api
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from youtube_dl import YoutubeDL
from redis import Redis
from rq import Queue, get_current_job
import downloader.download as dl
from pprint import pprint
import status
import os
import requests as req

basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
# app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + os.path.join(basedir, "videos.sqlite")
# app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
#
# db = SQLAlchemy(app)
# ma = Marshmallow(app)

api = Api(app)

# class Video(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     title = db.Column(db.String(150), unique=True)
#     description = db.Column(db.String(500))
#     url = db.Column(db.String(255), unique=True)
#
#     def __init__(self, title, description, url):
#         self.title = title
#         self.description = description
#         self.url = url
#
# class VideoSchema(ma.Schema):
#     class Meta:
#         fields = ("id", "title", "description", "url")
#
# video_schema = VideoSchema()
# videos_schema = VideoSchema(many=True)

class HelloWorld(Resource):
    def get(self):
        return {"hello": "world"}

videos = {}

r = Redis()
q = Queue(connection=r)

r.mset({"currentTaskProgress": 0})

current_prog = [0]
current_job = [None]

class RyAPIStatus(Resource):
    def get(self, video_url):
        global current_job
        if current_job[0].result == None:
            return {"status": req.get("http://127.0.0.1:4999/").json()}
        else:
            return {"status": "finished"}

class RyAPIStatusAlt(Resource):
    def get(self):
        global current_job
        if not current_job[0].is_finished:
            return {"status": "ongoing"}
        elif current_job[0].is_finished:
            return {"status": "finished"}

class RyAPIStatusImpl(Resource):

    def get(self, video_url):
        pass

class RyAPIAlt(Resource):
    def get(self):
        pass

    def post(self):
        job = q.enqueue(dl.download, request.form["v"])
        global current_job
        current_job[0] = job
        return {"status": "SUCC", "progress": f"status/{job.get_id()}"}


class RyAPI(Resource):
    def get(self, video_url):
        return videos[video_url]

    def post(self, video_url):
        if not video_url in videos.keys():
            videos[video_url] = request.form["v"]
        else:
            return {"status": "ERR", "msg": "Video already downloaded"}
        print(videos[video_url])
        #result = q.enqueue(download.rDown, request.form["v"])
        result = q.enqueue(dl.download, videos[video_url], job_timeout="1h")
        global current_job
        current_job[0] = result
        pprint(f"Task {result.id} enqued at {result.enqueued_at}\n{len(q)} jobs")
        #download.rDown(request.form["v"])
        return { "status": "SUCC", "progress": f"status/{video_url}"}


class RyAPIImpl(Resource):
    def get(self):
        return videos


# @app.route("/api", methods=["POST"])
# def add_video():
#     title = request.json["title"]
#     desc = request.json["description"]
#     url = request.json["url"]
#
#     new_video = Video(title, desc, url)
#     db.session.add(new_video)
#     db.session.commit()
#
#     return


api.add_resource(RyAPI, "/api/<string:video_url>")
api.add_resource(RyAPIStatus, "/status/<string:video_url>")
api.add_resource(HelloWorld, "/helloworld")

api.add_resource(RyAPIAlt, "/alt")
api.add_resource(RyAPIStatusAlt, "/alt/status")

@app.route("/")
def index():
    return render_template("main.html", token="Hello Flask-React")

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")