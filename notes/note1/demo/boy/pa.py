import random
import sys
from functools import reduce
from abc import ABCMeta, abstractmethod
from types import MethodType, FunctionType

sys.setrecursionlimit(10000)
li = list(range(10000))
random.shuffle(li)


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
        for j in range(i, len(data)):
            if data[min_index] > data[j]:
                min_index = j
        if min_index != i:
            data[i], data[min_index] = data[min_index], data[i]


def insert_sort(data):
    for i in range(1, len(data)):
        insert_num = data[i]
        b_index = i - 1
        while b_index >= 0 and data[b_index] > insert_num:
            data[b_index+1] = data[b_index]
            b_index -= 1
        data[b_index+1] = insert_num


def qucik_sort(data):
    if len(data) < 2:
        return data

    mid = data[0]
    larger = [i for i in data[1:] if i > mid]
    smarll = [i for i in data[1:] if i <= mid]
    return qucik_sort(smarll) + [mid] + qucik_sort(larger)


class Foo(object):
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(Foo, cls).__new__(cls, *args, **kwargs)
        return cls._instance


def single(cls):
    _instance = {}

    def inner(*args, **kwargs):
        if cls not in _instance:
            _instance[cls] = cls(*args, **kwargs)
        return _instance
    return inner


@single
class Boo(object):

    def func(self):
        pass


# class F(metaclass=ABCMeta):
#     @abstractmethod
#     def f(self):
#         pass


class A(object):pass
class B(object):pass
class C(object):pass
class E(A,B):pass
class F(A,B,C):pass
class G(E,F,C):pass

print(G.mro())

'''
mro(G) = G + merge(mro(E)+mro(F)+mor(C)+EFC)
mor(E) = E + merge(mro(A)+mro(B)+AB)
       = E + merge(A+B+AB)
       = E + AB 
       = EAB
mro(F) = F + merge(mro(A)+mro(B)+mro(C)+ABC)
       = F + merge(A + B + C +ABC)
       = F + ABC
       = FABC
mro(G) = G + merge(EAB+FABC+C+EFC)
       = G + (B+BC+C+C)
       = G + EFABC + object



'''