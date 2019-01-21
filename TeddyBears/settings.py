import os


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
