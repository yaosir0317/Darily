import time
import requests


boo = None
data_list = []
url = "https://www.lagou.com/jobs/positionAjax.json?city=%E5%8C%97%E4%BA%AC&needAddtionalResult=false"
header = {
    "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.110 Safari/537.36",
    "Accept": "application/json, text/javascript, */*; q=0.01",
    "Accept-Encoding": "gzip, deflate, br",
    "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
    "Connection": "keep-alive",
    "Content-Length": "26",
    "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
    "Cookie": "_ga=GA1.2.2128988071.1547120372; user_trace_token=20190110193936-686e9ada-14cc-11e9-95e8-525400f775ce; LGUID=20190110193936-686e9fdf-14cc-11e9-95e8-525400f775ce; index_location_city=%E5%8C%97%E4%BA%AC; JSESSIONID=ABAAABAAADEAAFIC23CA2C5D603BE8E59FABA9B5D6CE0E8; _gid=GA1.2.360634982.1551435677; _gat=1; Hm_lvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1550111375,1550663260,1551435679,1551438042; LGSID=20190301190045-437b3028-3c11-11e9-b354-525400f775ce; PRE_UTM=; PRE_HOST=www.baidu.com; PRE_SITE=https%3A%2F%2Fwww.baidu.com%2Flink%3Furl%3DoxCQqJNSqd63mOfY4MYE6bDK9n2194nElwcTsA05Sf3%26ck%3D3730.2.82.401.246.516.256.298%26shh%3Dwww.baidu.com%26sht%3D98012088_9_dg%26wd%3D%26eqid%3Daf1f473b00034bd6000000025c7910d5; PRE_LAND=https%3A%2F%2Fwww.lagou.com%2F; SEARCH_ID=821daff5ea72491582a9af646844ab56; LGRID=20190301190132-5f5396bf-3c11-11e9-b354-525400f775ce; Hm_lpvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1551438108; TG-TRACK-CODE=search_code",
    "Host": "www.lagou.com",
    "Origin": "https://www.lagou.com",
    "Referer": "https://www.lagou.com/jobs/list_python?labelWords=&fromSearch=true&suginput=",
    "X-Anit-Forge-Code": "0",
    "X-Anit-Forge-Token": "",
    "X-Requested-With": "XMLHttpRequest",
}
base_url = "https://www.lagou.com/jobs/%s.html"

for i in range(1, 31):
    if i == 1:
        boo = 'true'
    else:
        boo = 'false'
    data = {
        "first": boo,
        "pn": i,
        "kd": "python"
    }
    proxy = {
        "http": "139.217.24.50:3128"
    }
    req_data = requests.post(url=url, data=data, headers=header, proxies=proxy).json()
    data_list.append(req_data)
    time.sleep(1)
    print(req_data)
    break

f = open("lagou.csv", "w", encoding="utf8")
for data in data_list:
    dic = {}
