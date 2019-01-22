from flask import Blueprint
from flask import jsonify
from flask import request
from settings import Mongo_DB
from settings import RESULT
from bson import ObjectId

users = Blueprint("users", __name__)


@users.route("/reg", methods=["POST"])
def reg():
    user_info = request.form.to_dict()
    user_info["avatar"] = "mama.jpg" if user_info.get(
        "gender") == "1" else "baba.jpg"

    user_info["friend_list"] = []
    user_info["bind_toy"] = []

    res = Mongo_DB.users.insert_one(user_info)

    RESULT["code"] = 0
    RESULT["msg"] = "用户注册成功"
    RESULT["data"] = {"user_id": str(res.inserted_id)}

    return jsonify(RESULT)


@users.route("/login", methods=["POST"])
def login():
    user_info = request.form.to_dict()
    print(user_info)

    # {username:",password:"}
    user = Mongo_DB.users.find_one(user_info, {"password": 0})
    print(user)
    user["_id"] = str(user.get("_id"))

    RESULT["error_not"] = 0
    RESULT["msg"] = "用户登录"
    RESULT["data"] = user

    return jsonify(RESULT)


@users.route("/auto_login", methods=["POST"])
def auto_login():
    user_id = request.form.to_dict()
    user_id["_id"] = ObjectId(user_id.get("_id"))

    user = Mongo_DB.users.find_one(user_id, {"password": 0})
    user["_id"] = str(user_id.get("_id"))

    RESULT["error_not"] = 0
    RESULT["msg"] = "用户自动登录"
    RESULT["data"] = user

    return jsonify(RESULT)
