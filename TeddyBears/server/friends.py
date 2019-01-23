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
