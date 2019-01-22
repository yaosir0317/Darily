import requests


def pa():
    get_content = requests.get("http://36.7.87.209:8088/online/roomResource.xp?action=showResource")


print(pa())
# 生命之息 100
# 蓝色小 20
# 下级  30


# 精神 = 生命之息*10 + 蓝色魔力*10 = 7000
# 蓝色魔力 = 魔力结晶*1 + 蓝色小*10 = 600
# 魔力结晶 = 生命之息*1 + 下级*10  = 400
