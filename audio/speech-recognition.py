from aip import AipSpeech
from aip import AipNlp

""" 你的 APPID AK SK """
APP_ID = '15420587'
API_KEY = 'yZIj62YKphNlgRTKLKqE3E97'
SECRET_KEY = 'mIw24GX2pIwhUuE9TjlHqknIHkEaiD9O'

client = AipSpeech(APP_ID, API_KEY, SECRET_KEY)
npl = AipNlp(APP_ID, API_KEY, SECRET_KEY)

# 读取文件
def get_file_content(filePath):
    with open(filePath, 'rb') as fp:
        return fp.read()


# 识别本地文件
# ret = client.asr(get_file_content('123_0.wav'), 'wav', 16000, {
#     'dev_pid': 1536,
# })
# print(ret)

res = npl.simnet("中国队,大败美国队", "中国队大败,美国队")
print(res)
 