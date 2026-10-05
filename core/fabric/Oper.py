import inspect

# --- 1. Декоратор ---
def SetOper(label: str = None, order: int = 0, headOper: str = None, 
            isVisible: bool = True, icon: str = None, shortcut: str = None, 
            isCheckable: bool = False, tooltip: str = None):
    def decorator(func):
        func._is_oper_handler = True
        func._oper_id = func.__name__
        func._oper_label = label or func._oper_id.replace('_', ' ').title()
        func._order = order
        func._headOper = headOper
        func._isVisible = isVisible
        func._icon_path = icon
        func._shortcut = shortcut
        func._isCheckable = isCheckable
        func._tooltip = tooltip
        return func
    return decorator

# --- 2. Реестр ---
class OperRegistry:
    def __init__(self):
        self._flat_ops = []

    def register(self, instance):
        self._flat_ops = []
        for name, method in inspect.getmembers(instance, predicate=inspect.ismethod):
            if getattr(method, '_is_oper_handler', False):
                self._flat_ops.append({
                    'id': method._oper_id,
                    'label': method._oper_label,
                    'order': method._order,
                    'headOper': method._headOper,
                    'isVisible': method._isVisible,
                    'icon': method._icon_path,
                    'shortcut': method._shortcut,
                    'checkable': method._isCheckable,
                    'tooltip': method._tooltip,
                    'handler': method
                })
        self._flat_ops.sort(key=lambda x: x['order'])

    def get_children(self, parent_id=None):
        # Для корневых элементов headOper должен быть None
        return [op for op in self._flat_ops 
                if op['isVisible'] and op['headOper'] == parent_id]