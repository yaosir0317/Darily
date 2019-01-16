from aip import AipSpeech, AipNlp
import os


""" 你的 APPID AK SK """
APP_ID = '15420336'
API_KEY = 'VwSGcqqwsCl282LGKnFwHDIA'
SECRET_KEY = 'h4oL6Y9yRuvmD0oSdQGQZchNcix4TF5P'

nlp = AipNlp(APP_ID, API_KEY, SECRET_KEY)
client = AipSpeech(APP_ID, API_KEY, SECRET_KEY)


# 读取audio文件
def get_file_content(audio):
    os.system(f"D:\\小工具\\ffmpeg\\bin\\ffmpeg -y  -i {audio} -acodec pcm_s16le -f s16le -ac 1 -ar 16000 audio.pcm")
    with open("audio.pcm", 'rb') as fp:
        return fp.read()


# audio转text
def audio2text(filePath):
    res = client.asr(get_file_content(filePath), 'pcm', 16000, {
        'dev_pid': 1536,
    })
    return res.get("result")[0]


# 图灵机器人处理问题
def to_tuling(question):
    import requests

    args = {
        "reqType": 0,
        "perception": {
            "inputText": {
                "text": question
            }
        },
        "userInfo": {
            "apiKey": "96713231d0504c90b96803e3146180e8",
            "userId": "1111"
        }
    }

    url = "http://openapi.tuling123.com/openapi/api/v2"

    res = requests.post(url, json=args)

    response = res.json().get("results")[0].get("values").get("text")

    return response


# text转audio
def text2audio(text):
    audio = client.synthesis(
        text, 'zh', 1, {
            'vol': 5,
            "per": 4,
            "pit": 6,
            "spd": 4
        })

    # 识别正确返回语音二进制 错误则返回dict 参照下面错误码
    if not isinstance(audio, dict):
        with open('audio.mp3', 'wb') as f:
            f.write(audio)

