from threading import Lock


# Thread-safe Singleton
class Singleton(type):
    _instances = {}

    _lock: Lock = Lock()

    def __call__(cls, *args, **kwargs):
        with cls._lock:
            if cls not in cls._instances:
                instance = super().__call__(*args, **kwargs)
                cls._instances[cls] = instance
        return cls._instances[cls]


# Naïve Singleton
# class Singleton(type):
#     def __init__(cls, name, bases, dictionary):
#         super(Singleton, cls).__init__(name, bases, dictionary)
#         cls.instance = None
#
#     def __call__(cls, *args, **kw):
#         if cls.instance is None:
#             cls.instance = super(Singleton, cls).__call__(*args, **kw)
#         return cls.instance
