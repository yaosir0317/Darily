from pymongo import MongoClient
from redis import Redis
from aip import AipSpeech
from aip import AipNlp

# 创建数据库
client = MongoClient(host="127.0.0.1", port=27017)
Mongo_DB = client["TeddyBears"]

REDIS_DB = Redis(host="127.0.0.1", port=6379, db=10)

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

BASE_URL = "http://192.168.13.204"
BASE_WS = "ws://192.168.13.204"

# 二维码路径
QR_PATH = "QRcode"

# 联图api
LT_URL = "http://qr.liantu.com/api.php?text=%s"

# 图灵
TULING_STR = {
        "reqType": 0,
        "perception": {
            "inputText": {
                "text": "%s"
            }
        },
        "userInfo": {
            "apiKey": "96713231d0504c90b96803e3146180e8",
            "userId": "%s"
        }
    }
TULING_URL = "http://openapi.tuling123.com/openapi/api/v2"

# baiduAi配置

""" 你的 APPID AK SK """
APP_ID = '15420336'
API_KEY = 'VwSGcqqwsCl282LGKnFwHDIA'
SECRET_KEY = 'h4oL6Y9yRuvmD0oSdQGQZchNcix4TF5P'

NLP = AipNlp(APP_ID, API_KEY, SECRET_KEY)
SPEECH = AipSpeech(APP_ID, API_KEY, SECRET_KEY)

VOICE = {
    'vol': 5,
    "spd": 4,
    "pit": 6,
    "per": 4
}
