from functools import wraps
from functools import reduce
import time
import copy
import os
import random


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
        half = half * 10 + num % 10
        num = num // 10
        print(half, num)
    return num == half or num == half // 10


ls = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
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


def dec1(func):

    def one():
        print("2222")
        func()
        print("3333")


    return one


def dec2(func):

    def two():
        print("1111")
        func()
        print("4444")

    return two


@dec1
@dec2
def test():
    print("test test")


def file_all(filepath, n):
    file_list = os.listdir(filepath)
    for item in file_list:
        cur_file = os.path.join(filepath, item)
        if os.path.isdir(cur_file):
            print("\t"*n, item)
            file_all(cur_file, n+1)
        else:
            print("\t"*n, item)


ls = list(range(10000))
# random.shuffle(ls)


def bubble_sort(data):
    for i in range(len(data)-1):
        exchange = False
        for j in range(len(data)-1-i):
            if data[j] > data[j+1]:
                data[j], data[j+1] = data[j+1], data[j]
                exchange = True
        if not exchange:
            break


def select_sort(data):
    for i in range(len(data)-1):
        min_index = i
        for j in range(i+1, len(data)):
            if data[min_index] > data[j]:
                min_index = j
        if min_index != i:
            data[min_index], data[i] = data[i], data[min_index]


def insert_sort(data):
    for i in range(1, len(data)):
        select = data[i]
        b_index = i - 1
        while b_index >= 0 and data[b_index] > select:
            data[b_index+1] = data[b_index]
            b_index -= 1
        data[b_index+1] = select


def quick_sort(data):
    if len(data) < 2:
        return data
    mid = data[0]
    larger = [i for i in data[1:] if i > mid]
    smaller = [i for i in data[1:] if i <= mid]
    return quick_sort(smaller) + [mid] + quick_sort(larger)


def bin_search(data, num):
    left = 0
    right = len(data)
    while left <= right:
        mid = (right + left) // 2
        if data[mid] == num:
            return mid
        elif data[mid] > num:
            right = mid - 1
        else:
            left = left + 1
    return -1


class A(object):
    def __getattr__(self, item):
        print(item)


# from flask import Flask, views
#
# app = Flask(__name__)
#
#
# class Login(views.MethodView):
#     def get(self,args):
#         args.method
#         return "666"
#
#     def post(self,args):
#         return "888"
#
#     def look(self,args):
#         return "999"
#
# app.add_url_rule("/login/<args>",endpoint=None,view_func=Login.as_view(name='login'))
# app.__call__

with open(r"D:\python-file\VUE\Daily\demo_2\rbac\models.py", "r") as f:
    for line in f:
        print(line)
