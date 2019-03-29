import time
import hashlib


class XunForward(object):
    """
    动态转发
    """

    orderno = "ZF20193102350AJChOj"
    secret = "787700caa34e4eb2911de0267b6be6ec"

    ip = "forward.xdaili.cn"
    port = "80"

    ip_port = ip + ":" + port
    # 计算时间戳
    timestamp = str(int(time.time()))

    _string = "orderno=" + orderno + "," + "secret=" + secret + "," + "timestamp=" + timestamp
    # 计算sign
    md5_string = hashlib.md5(_string.encode('utf-8')).hexdigest()
    # 转换成大写
    sign = md5_string.upper()
    auth = "sign=" + sign + "&" + "orderno=" + orderno + "&" + "timestamp=" + timestamp

    @classmethod
    def get_proxy_headers(cls):
        proxy = {"http": "http://" + cls.ip_port, "https": "https://" + cls.ip_port}
        headers = {"Proxy-Authorization": cls.auth}

        return proxy, headers


if __name__ == '__main__':
    proxy, headers = XunForward.get_proxy_headers()
    print(proxy, headers)
