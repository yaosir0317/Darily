import os
from flask import Blueprint
from flask import send_file

import settings

app_anything = Blueprint("app_anything", __name__)


@app_anything.route("/img/<filename>")
def get_img(filename):
    img_path = os.path.join(settings.IMG_PATH, filename)
    return send_file(img_path)


@app_anything.route("/music/<filename>")
def get_music(filename):
    music_path = os.path.join(settings.MUSIC_PATH, filename)
    return send_file(music_path)
