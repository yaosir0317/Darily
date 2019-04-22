from functools import wraps
from functools import reduce


def log(text=None):
    def outer(func):
        @wraps(func)
        def inner(*args, **kwargs):
            if text:
                print(text)
            print("begin call")
            ret = func(*args, **kwargs)
            print("end call")
            return ret
        return inner
    return outer


class A(object):

    def _f1(self, x):
        print(x)

    @classmethod
    def f2(cls, x):
        cls.__f3(x)

    @staticmethod
    def __f3(x):
        print(x)


class B(A):
    def f4(self, x):
        self._f1(x)


def shif():
    pass


def decorator(data):
    def outer(func):
        def inner(name, *args, **kwargs):
            if name in data:
                return func(name, *args, **kwargs)
        return inner
    return outer


ls = ["赵一宁", "春生"]


@decorator(ls)
def test(name, age):
    print(name, age)


test("赵一宁", 38)
