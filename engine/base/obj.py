import weakref

class BaseObj:
    _instances = weakref.WeakSet()

    def __init__(self):
        BaseObj._instances.append(self)

    @classmethod
    def get_all_instances(cls):
        return cls._instances.copy()