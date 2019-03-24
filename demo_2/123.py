from functools import wraps
from functools import reduce
import time
import copy
import os


def outer(func):
    dic = {}

    @wraps(func)
    def inner(*args, **kwargs):
        result = None
        key = func.__name__
        if key in dic:
            last_time = dic[key]
            limit = time.time() - last_time
            if limit < 10:
                print(f"try again in {int(10-limit)} seconds")
                result = 1
            else:
                result = None
                return func(*args, **kwargs)
        if not result:
            dic[key] = time.time()
            return func(*args, **kwargs)

    return inner

@outer
def foo(a):
    print(a)


@outer
def bar(a):
    print(a)


def isPalindromeself(num):
    if num < 0 or (num != 0 and num % 10 == 0):
        return False
    half = 0
    while half < num:
        half = half*10 + num%10
        num = num//10
        print(half, num)
    return num == half or num == half//10


ls = [[1,2,3],[4,5,6],[7,8,9]]
ret = []
for i in ls:
    ret += i


d = {"a": 26, "g": 20, "e": 20, "c": 24, "d": 23, "f": 21, "b": 25}
alist = [3, 1, -4, -2]
li = sorted(d.items(), key=lambda x: x[1])
# print(sorted(alist, key=lambda x: abs(x)))

a = [1, [2, 3]]
b = a
b[1].append(4)
c = copy.copy(a)
c.append(5)


def func(abc):
    dic = {}
    for i in list(abc):
        if i in dic:
            dic[i] += 1
        else:
            dic[i] = 1
    print(set(dic.values()))
    if len(set(dic.values())) == 1:
        return True
    return False


x = "abcabccba"
# print(func(x))


def outer1(func):
    dic = 0

    def inner(*args, **kwargs):
        nonlocal dic
        now = time.time()
        if now - dic > 10:
            dic = now
            return func(*args, **kwargs)
        else:
            print("太快了")
    return inner


v = "10.3.9.12"
def func(ip):
    ret = ""
    for i in v.split("."):
        ret += bin(int(i))[2:].zfill(8)
    return int(ret, 2)


print(reduce(lambda x, y: x*y, range(1, 4)))