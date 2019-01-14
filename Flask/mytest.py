from flask import Flask
from flask import redirect
from flask import render_template
from flask import jsonify
from flask import send_file
from flask import request
from flask import session
from flask import Markup
from flask import views
from flask import Blueprint

from functools import wraps
from flask_session import Session
from wtforms import simple, core

# AssertionError: View function mapping is overwriting an existing endpoint function: inner

api = Flask(__name__)
api.secret_key = "good night!"


def login_access(fun):
    @wraps(fun)
    def inner(*args, **kwargs):
        if not session.get("user_key"):
            return redirect("/login")
        return fun(*args, **kwargs)
    return inner


@api.template_global()
def func(a, b):
    return a+b


@api.template_filter()
def fil(a, b, c):
    return a+b+c


tag = Markup("<input type='text' name='username'>")


@api.route("/")
@login_access
def index():
    return render_template("index.html", tag=tag)


@api.route("/login", methods=["POST", "GET"])
def login():
    print(request.method)
    print(request.form)
    print(request.form.to_dict())
    print(request.args)
    print(request.url)
    print(request.path)
    print(request.host)
    print(request.cookies)
    if request.method == "GET":
        print("=========================================")
        return render_template("login.html")
    elif request.form.to_dict().get("username") == "123" and request.form.to_dict().get("password") == "123":
        session["user_key"] = "The philosophers have only interpreted the world in various ways" \
                              " - the point however is to change it"
        return redirect("/")
    return "登录失败"


@api.route("/home")
@login_access
def home():
    ret = {"name": "yao"}
    return jsonify(ret)


@api.route("/file")
@login_access
def file():
    return send_file("D:\腾讯QQ文件\段子\girls.jpg")


@api.route("/req")
@login_access
def req():
    print(request.path)
    return render_template("req.html")


class Book(views.MethodView):
    def get(self, num):
        return render_template("req.html", num=num)

    def post(self, num):
        return "123"


api.add_url_rule("/book/<num>", view_func=Book.as_view("my_book"))


app01 = Blueprint("app01", __name__, url_prefix="/blue")


@app01.route("/blue")
def func_app():
    return "blueprint"


api.register_blueprint(app01)


@api.errorhandler(404)
def err(error_info):
    return error_info


api.run(debug=True)
