from bson import ObjectId

from flask import Blueprint
from flask import jsonify
from flask import request

from settings import Mongo_DB
from settings import RESULT

devices = Blueprint("devices", __name__)


# 玩具是否授权
@devices.route("/validateCode", methods=["POST"])
def validate_code():
    code = request.form.to_dict()  # device_key
    res = Mongo_DB.devices.find_one(code, {"_id": 0})

    if res:
        RESULT["error_not"] = 0
        RESULT["msg"] = "设备已授权，开启绑定"
        RESULT["data"] = res
        # 添加好友逻辑
    else:
        RESULT["error_not"] = 2
        RESULT["msg"] = "非授权设备"
        RESULT["data"] = {}

    return jsonify(RESULT)


# 玩具绑定
@devices.route("/bindToy", methods=["POST"])
def bind_toy():
    # toys.bind_user = "user_id"
    # users.bind_toy = ["toy_id"]
    # 1.device_key 2.fromdata 3. who bind toy
    toy_info = request.form.to_dict()

    # 创建聊天窗口
    chat_window = Mongo_DB.chats.insert_one({"user_list": [], "chat_list": []})

    # 通过user_id去查询用户信息 谁绑定玩具
    user_info = Mongo_DB.users.find_one({"_id": ObjectId(toy_info["user_id"])})

    toy_info["bind_user"] = toy_info.pop("user_id")
    toy_info["avatar"] = "toy.png"
    # 自然逻辑 好友关系
    toy_info["friend_list"] = [
        {
            "friend_id": toy_info["bind_user"],
            "friend_name": user_info.get("nickname"),
            "friend_nick": toy_info.pop("remark"),
            "friend_avatar": user_info.get("avatar"),
            "friend_type": "app",
            "friend_chat": str(chat_window.inserted_id)
        }
    ]

    toy = Mongo_DB.toys.insert_one(toy_info)

    # 用户添加绑定玩具 及 自然逻辑 好友关系
    user_info["bind_toy"].append(str(toy.inserted_id))
    user_add_toy = {
        "friend_id": str(toy.inserted_id),
        "friend_name": toy_info.get("toy_name"),
        "friend_nick": toy_info.get("baby_name"),
        "friend_avatar": toy_info.get("avatar"),
        "friend_type": "toy",
        "friend_chat": str(chat_window.inserted_id)
    }

    user_info["friend_list"].append(user_add_toy)

    Mongo_DB.users.update_one({"_id": ObjectId(toy_info["bind_user"])}, {"$set": user_info})
    Mongo_DB.chats.update_one({"_id": chat_window.inserted_id}, {"$set": {"user_list": [
        str(toy.inserted_id), str(user_info.get("_id"))
    ]}})

    RESULT["error_not"] = 0
    RESULT["msg"] = "绑定玩具成功"
    RESULT["data"] = {}

    return jsonify(RESULT)


# 通过user_id获取绑定的玩具
@devices.route("/toyList", methods=["POST"])
def toy_list():
    # bind_toy : [Obj("toy_id"),"toy_id2"]

    user_id = request.form.get("user_id")
    user_info = Mongo_DB.users.find_one({"_id": ObjectId(user_id)})
    user_bind_toy = user_info.get("bind_toy")

    for index, item in enumerate(user_bind_toy):
        user_bind_toy[index] = ObjectId(item)

    toy_l = list(Mongo_DB.toys.find({'_id': {"$in": user_bind_toy}}))

    for index, toy in enumerate(toy_l):
        toy_l[index]["_id"] = str(toy.get("_id"))

    RESULT["error_not"] = 0
    RESULT["msg"] = "查看所有绑定玩具"
    RESULT["data"] = toy_l

    return jsonify(RESULT)


@devices.route("/device_login", methods=["POST"])
def device_login():
    dev_info = request.form.to_dict()
    dev = Mongo_DB.devices.find_one(dev_info)
    if dev:
        toy = Mongo_DB.toys.find_one(dev_info)
        if toy:
            return jsonify({"music": "欢迎来到智能亲子互动乐园", "info": str(toy.get("_id"))})
        return jsonify({"info": "请对我进行绑定后再玩耍"})
    else:
        return jsonify({"info": "请联系玩具经销商"})
