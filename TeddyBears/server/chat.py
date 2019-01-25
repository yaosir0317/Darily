from flask import Blueprint
from flask import send_file
from flask import request
from flask import jsonify

from settings import Mongo_DB
from settings import RESULT
from redis_msg import get_reids_one, get_redis_all


chat = Blueprint("chat", __name__)


@chat.route("/recv_msg", methods=["POST"])
def recv_msg():
    to_user = request.form.get("to_user")
    from_user = request.form.get("from_user")
    count = get_reids_one(to_user, from_user)  # 3
    chat_window = Mongo_DB.chats.find_one(
        {"user_list": {"$all": [to_user, from_user]}})
    # chat = chat_window.get("chat_list")[-count:]
    chat_lists = []
    for chats in reversed(chat_window.get("chat_list")):
        if chats.get("sender") != from_user:
            continue
        chat_lists.append(chat)
        if len(chat_lists) == count:
            break
    chat_lists.reverse()
    return jsonify(chat_lists)


@chat.route("/chat_list", methods=["POST"])
def chat_list():
    to_user = request.form.get("to_user")
    from_user = request.form.get("from_user")

    print(to_user, from_user)
    chat_window = Mongo_DB.chats.find_one(
        {"user_list": {"$all": [to_user, from_user]}})

    get_reids_one(to_user, from_user)

    RESULT["error_not"] = 0
    RESULT["msg"] = "查询聊天内容"
    RESULT["data"] = chat_window.get("chat_list")[-10:]

    return jsonify(RESULT)


@chat.route("/chat_count", methods=["POST"])
def chat_count():
    user_id = request.form.get("user_id")
    to_user_msg = get_redis_all(user_id)

    RESULT["error_not"] = 0
    RESULT["msg"] = "查询未读消息"
    RESULT["data"] = to_user_msg

    return jsonify(RESULT)
