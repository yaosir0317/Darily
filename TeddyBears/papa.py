import time


def outer(func):
    def inner(*args, **kwargs):
        start = time.time()
        ret = func(*args, **kwargs)
        end = time.time()
        print(end-start)
        return ret
    return inner


@outer
def cal(n):
    for i in range(1000**2*n):
        continue
    return 123


class A(object):

    def __init__(self, num):
        self.num = num

    def func(self):
        print(self.num)


class B(A):

    def __func2(self):
        print(self.num, 123)

    def func3(self):
        self.__func2()

    def func4(self):
        self.func()


class Animal(object):
    def __init__(self, name):
        self.name = name

    def eating(self):
        print(self.name + "can eating")

    def drinking(self):
        print(self.name + "can drinking")


class Cat(Animal):
    def __init__(self, name, sound):
        super().__init__(name)
        self.sound = sound

    def cat_sound(self):
        print("喵")


class Dog(Animal):
    def dog_sound(self):
        print("汪")


obj = Cat("猫", "喵")

print(obj.name)


class Foo(object):

    def get_bar(self):
        print('属性')

    # *必须两个参数
    def set_bar(self, value):
        print('set value' + value)

    def del_bar(self):
        print('property')

    BAR = property(get_bar, set_bar, del_bar, '131313')