import inspect

from core.decorator import TypeDecorator


class OperRegistry:
    """Реестр операций и сеттеров класса"""

    def __init__(self, cls):
        self.cls = cls
        self._flat_ops = []
        self._flat_ops_handler = {}
        self._oper()

    def _oper(self):
        self._flat_ops = []
        self._flat_ops_handler = {}
        for name, method in inspect.getmembers(self.cls, predicate=inspect.ismethod):
            if getattr(method, "_type", False) == TypeDecorator.Oper:
                self._flat_ops.append(
                    {
                        "id": method._id,
                        "label": method._oper_label,
                        "order": method._order,
                        "headOper": method._headOper,
                        "isVisible": method._isVisible,
                        "isDisabled": method._isDisabled,
                        "icon": method._icon_path,
                        "shortcut": method._shortcut,
                        "checkable": method._isCheckable,
                        "tooltip": method._tooltip,
                    }
                )

                self._flat_ops_handler[method._id] = method

        self._flat_ops.sort(key=lambda x: x["order"])

    def get_children_oper(self, parent_id=None):
        # Для корневых элементов headOper должен быть None
        return [
            op | {"child": self.get_children_oper(op['id'])}
            for op in self._flat_ops
            if op["isVisible"] and op["headOper"] == parent_id
        ]

    def get_oper(self)->list[dict]:
        return self._flat_ops

    def _set_attr(self, nameAttr:str, name:str|list[str], value)->None:
        if isinstance(name, str): name = [name]
        for item in self._flat_ops:
            if item['id'] in name:
                item[nameAttr] = value

    def isDisabled(self, name:str|list[str], value)->None:
        self._set_attr('isDisabled', name, value)

    def isVisible(self, name:str|list[str], value)->None:
        self._set_attr('isVisible', name, value)
