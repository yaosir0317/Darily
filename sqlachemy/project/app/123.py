# def dec1(func):
#     print("1111")
#
#     def one():
#         print("2222")
#         func()
#         print("3333")
#     return one
#
#
# def dec2(func):
#     print("aaaa")
#
#     def two():
#         print("bbbb")
#         func()
#         print("cccc")
#     return two
#
#
# @dec1
# @dec2
# def test():
#     print("test test")
#
#
# test()
#
# '''
# 1111
# 2222
# aaaa
# bbbb
# test test
# cccc
# 3333
#
# '''


# print([chr(i) for i in range(97, 123)])

import redis
# session["key"] = "value"
re = redis.Redis(host="127.0.0.1", port=6379, db=6)
print(re.get("session:63470f4c-3b74-4cb8-8db0-8cdf50c0643e"))
