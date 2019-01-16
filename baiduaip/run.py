from flask import Flask
from flask import render_template
from flask import jsonify
from flask import request
from flask import send_file

import pymongo

import api


mongo_client = pymongo.MongoClient(host="127.0.0.1", port=27017)
MongoDB = mongo_client["chats"]


def append_chat(data):

    MongoDB.user.update({"id": 1}, {"$push": {"chat_list": data}})


app = Flask(__name__, template_folder="templates")


@app.route("/")
def index():

    return render_template("index.html")


@app.route("/get_audio/audio.mp3")
def get_audio():
    return send_file("audio.mp3")


@app.route("/ai", methods=["POST"])
def ai():
    # 1.保存录音文件
    audio = request.files.get("record")
    filename = "audio.wav"
    audio.save(filename)

    # 2.将录音文件转换为PCM发送给百度进行语音识别
    question_text = api.audio2text(filename)
    append_chat({"user": question_text})
    # 3.将识别的问题交给图灵或自主处理获取答案
    response_text = api.to_tuling(question_text)
    append_chat({"tuling": response_text})
    # 4.将答案发送给百度语音合成，合成音频文件
    result_file = api.text2audio(response_text)

    # 5.将音频文件发送给前端播放

    return jsonify({"filename": result_file})


if __name__ == '__main__':

    app.run("0.0.0.0", 9527, debug=True)
