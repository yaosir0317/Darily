import os
from uuid import uuid4

from flask import Blueprint
from flask import send_file
from flask import request
from flask import jsonify

import settings
from settings import RESULT

app_anything = Blueprint("app_anything", __name__)


# 歌曲封面链接
@app_anything.route("/img/<filename>")
def get_img(filename):
    img_path = os.path.join(settings.IMG_PATH, filename)
    return send_file(img_path)


# 歌曲播放链接
@app_anything.route("/music/<filename>")
def get_music(filename):
    music_path = os.path.join(settings.MUSIC_PATH, filename)
    return send_file(music_path)


# 语音链接
@app_anything.route("/chat/<filename>")
def get_chat(filename):
    file_path = os.path.join(settings.CHAT_PATH, filename)
    return send_file(file_path)


# 将接受的音频转换MP3
@app_anything.route("/uploader", methods=["POST"])
def uploader():
    audio = request.files.get("recorder")
    import os
    path = os.path.join(settings.CHAT_PATH, audio.filename)
    audio.save(path)
    os.system(f"D:\\小工具\\ffmpeg\\bin\\ffmpeg -i {path} {path}.mp3")

    RESULT["error_not"] = 0
    RESULT["msg"] = "上传音频文件"
    RESULT["data"] = {"filename": f"{audio.filename}.mp3"}

    return jsonify(RESULT)


@app_anything.route("/toy_uploader", methods=["POST"])
def toy_uploader():
    audio = request.files.get("record")
    filename = f"{uuid4()}.wav"
    import os
    path = os.path.join(settings.CHAT_PATH, filename)
    audio.save(path)
    # os.system(f"ffmpeg -i {path} {path}.mp3")

    return jsonify({"code": 0, "filename": filename})
