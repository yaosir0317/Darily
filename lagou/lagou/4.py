import threading


class Singleton(type):
    _instance_lock = threading.Lock()

    def __call__(cls, *args, **kwargs):
        if not hasattr(cls, "_instance"):
            with Singleton._instance_lock:
                if not hasattr(cls, "_instance"):
                    cls._instance = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instance


class A(metaclass=Singleton):
    def func(self):
        pass


obj1 = A()
obj2 = A()
print(id(obj1))
print(id(obj2))