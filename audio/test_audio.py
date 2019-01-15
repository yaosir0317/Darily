from aip import AipSpeech

""" 你的 APPID AK SK """
APP_ID = '15420587'
API_KEY = 'yZIj62YKphNlgRTKLKqE3E97'
SECRET_KEY = 'mIw24GX2pIwhUuE9TjlHqknIHkEaiD9O'

client = AipSpeech(APP_ID, API_KEY, SECRET_KEY)


result = client.synthesis(
    '茕茕孑立沆瀣一气,踽踽独行醍醐灌顶,绵绵瓜瓞奉为圭臬,龙行龘龘犄角旮旯,娉婷袅娜涕泗滂沱,呶呶不休不稂不莠', 'zh', 1, {
        'vol': 5,
        "per": 4,
        "pit": 6,
        "spd": 4
    })

# 识别正确返回语音二进制 错误则返回dict 参照下面错误码
if not isinstance(result, dict):
    with open('audio.mp3', 'wb') as f:
        f.write(result)
