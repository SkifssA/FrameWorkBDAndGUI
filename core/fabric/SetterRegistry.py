import inspect

from core.decorator import TypeDecorator


class SetterRegistry:
    """Реестр операций и сеттеров класса"""

    def __init__(self, cls):
        self.cls = cls
        self._flat_set = []
        self._flat_set_handler = {}
        self._setter()

    def _setter(self):
        self._flat_set = []
        self._flat_set_handler = {}
        for name, method in inspect.getmembers(self.cls, predicate=inspect.ismethod):
            if getattr(method, "_type", False) == TypeDecorator.Setter:
                self._flat_set.append({
                    'id': method._id
                })
                
                self._flat_set_handler[method._id] = {
                    "method": method
                }

    def get_setter(self):
        return self._flat_set
