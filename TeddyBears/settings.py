from pymongo import MongoClient


# 创建数据库
client = MongoClient(host="127.0.0.1", port=27017)
Mongo_DB = client["TeddyBears"]


# rest-api
RESULT = {
    "error_not": 0,
    "msg": "",
    "data": {}
}

# 歌曲路径
MUSIC_PATH = "music"
# 图像路径
IMG_PATH = "img"
# 语音路径
CHAT_PATH = "chat"

BASE_URL = "http://192.168.13.102"
BASE_WS = "ws://192.168.13.102"

# 二维码路径
QR_PATH = "QRcode"

# 联图api
LT_URL = "http://qr.liantu.com/api.php?text=%s"
