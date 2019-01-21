from uuid import uuid4
import os
import time

import requests

import settings

base_img_url = "http://audio.xmcdn.com/"
url = "http://m.ximalaya.com/m-revision/page/track/queryTrackPage/%s"

info_list = ["ertong/5194595/21018150", "ertong/5194595/21018195",
             "ertong/5194595/21017396", "ertong/5194595/21019175",
             "ertong/5194595/21018328", "ertong/5194595/21018340"
             ]


def get_info_by_requests(content_list):
    information = []

    for el in content_list:
        # 获取当前采集id
        audio_id = el.rsplit("/", 1)[-1]
        audio_get_content = requests.get(url%(audio_id))
        # 采集信息
        audio_get_dict = audio_get_content.json().get("data").get("trackDetailInfo").get("trackInfo")

        # 获取信息内需要的内容
        audio_url = audio_get_dict.get("playPath")
        audio_img_url = base_img_url + audio_get_dict.get("cover")
        audio_name = audio_get_dict.get("title")
        audio_info = audio_get_dict.get("intro")
        audio_img = requests.get(audio_img_url)
        audio = requests.get(audio_url)

        # 拼接图片与歌曲的路径和名称
        filename = uuid4()
        img = os.path.join(settings.IMG_PATH, f"{filename}.jpg")
        music = os.path.join(settings.MUSIC_PATH, f"{filename}.mp3")

        # 保存图片
        with open(img, "wb") as f:
            f.write(audio_img.content)
        # 保存歌曲
        with open(music, "wb") as g:
            g.write(audio.content)

        # 建立写入数据库
        music_info = {
            "title": audio_name,
            "info": audio_info,
            "img": f"{filename}.jpg",
            "music": f"{filename}.mp3"
        }

        information.append(music_info)
        time.sleep(1)

    settings.Mongo_DB.TeddyBears.insert_many(information)


get_info_by_requests(info_list)
