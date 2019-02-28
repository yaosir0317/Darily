from flask import session
from flask import render_template
from flask import Flask
from flask import request
from flask_session import Session
import redis

app = Flask(__name__, template_folder="templates")
app.config["SESSION_TYPE"] = "redis"
app.config["SESSION_REDIS"] = redis.Redis(host="127.0.0.1",port=6379,db=6)

Session(app)


@app.route("/", methods=["POST", "GET"])
def func():
    if request.method == "GET":
        return render_template("login.html")
    if request.method == "POST":
        session["key"] = "value"
        return "123"


app.run()