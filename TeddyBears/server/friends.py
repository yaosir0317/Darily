from bson import ObjectId

from flask import Blueprint
from flask import jsonify
from flask import request

from settings import Mongo_DB
from settings import RESULT


friends = Blueprint("friends", __name__)


# 通过user_id获取其好友列表,绑定的玩具
@friends.route("/friendList", methods=["POST"])
def friend_list():
    user_id = ObjectId(request.form.get("user_id"))  # 字符串user_id转objectId
    user_info = Mongo_DB.users.find_one({"_id": user_id})

    RESULT["error_not"] = 0
    RESULT["msg"] = "好友列表查询"
    RESULT["data"] = user_info.get("friend_list")

    return jsonify(RESULT)


@friends.route("/add_req", methods=["POST"])
def add_req():
    req_info = request.form.to_dict()
    if req_info.get("friend_type") == "app":
        user_info = Mongo_DB.users.find_one(
            {"_id": ObjectId(req_info.get("add_user_id"))})
    else:
        user_info = Mongo_DB.toys.find_one(
            {"_id": ObjectId(req_info.get("add_user_id"))})

    req_info["req_avatar"] = user_info.get("avatar")
    req_info["add_user_nick"] = user_info.get("nickname") if user_info.get(
        "nickname") else user_info.get("baby_name")

    Mongo_DB.request.insert_one(req_info)

    RESULT["error_not"] = 0
    RESULT["msg"] = "请求添加成功"
    RESULT["data"] = {}

    return jsonify(RESULT)


@friends.route("/acc_req", methods=["POST"])
def acc_req():
    req_id = request.form.get("req_id")
    remark = request.form.get("remark")
    req_info = Mongo_DB.request.find_one({"_id": ObjectId(req_id)})
    print(req_info)
    print(req_info)
    user_info = Mongo_DB.users.find_one(
        {"_id": ObjectId(req_info.get("add_user_id"))})
    if not user_info:
        user_info = Mongo_DB.toys.find_one(
            {"_id": ObjectId(req_info.get("add_user_id"))})

    toy_info = Mongo_DB.toys.find_one(
        {"_id": ObjectId(req_info.get("firend_id"))})

    chat_info = {
        "user_list": [str(user_info.get("_id")), str(toy_info.get("_id"))],
        "chat_list": []
    }
    chat_window = Mongo_DB.chats.insert_one(chat_info)

    user_add_toy = {
        "friend_id": str(toy_info.get("_id")),
        "friend_name": toy_info.get("toy_name"),
        "friend_nick": req_info.get("friend_remark"),
        "friend_avatar": "toy.jpg",
        "friend_type": "toy",
        "friend_chat": str(chat_window.inserted_id)
    }

    user_info["friend_list"].append(user_add_toy)

    toy_add_user = {
        "friend_id": str(
            user_info.get("_id")),
        "friend_name": user_info.get("nickname") if user_info.get("nickname") else user_info.get("toy_name"),
        "friend_nick": remark,
        "friend_avatar": user_info.get("avatar"),
        "friend_type": "app" if user_info.get("nickname") else "toy",
        "friend_chat": str(
            chat_window.inserted_id)}
    toy_info["friend_list"].append(toy_add_user)

    if user_info.get("nickname"):
        Mongo_DB.users.update_one(
            {"_id": ObjectId(req_info.get("add_user_id"))}, {"$set": user_info})
    else:
        Mongo_DB.toys.update_one(
            {"_id": ObjectId(req_info.get("add_user_id"))}, {"$set": user_info})

    Mongo_DB.toys.update_one({"_id": ObjectId(req_info.get("firend_id"))},
                             {"$set": toy_info})

    Mongo_DB.request.update_one({"_id": ObjectId(req_id)}, {
                            "$set": {"status": 1}})

    RESULT["error_not"] = 0
    RESULT["msg"] = "添加好友成功"
    RESULT["data"] = {}

    return jsonify(RESULT)


@friends.route("/ref_req", methods=["POST"])
def ref_req():
    req_id = request.form.get("req_id")
    Mongo_DB.request.update_one({"_id": ObjectId(req_id)}, {
                                "$set": {"status": 2}})

    RESULT["error_not"] = 0
    RESULT["msg"] = "拒绝好友请求"
    RESULT["data"] = {}

    return jsonify(RESULT)


@friends.route("/req_list", methods=["POST"])
def req_list():
    user_id = request.form.get("user_id")
    user_info = Mongo_DB.users.find_one({"_id": ObjectId(user_id)})
    user_bind_toy = user_info.get("bind_toy")

    req_li = list(Mongo_DB.request.find({"firend_id": {"$in": user_bind_toy}}))

    for index, item in enumerate(req_li):
        req_li[index]["_id"] = str(item.get("_id"))

    RESULT["error_not"] = 0
    RESULT["msg"] = "查询好友请求"
    RESULT["data"] = req_li

    return jsonify(RESULT)
