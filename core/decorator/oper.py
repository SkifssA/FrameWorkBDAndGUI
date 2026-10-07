OPER = 'oper'

def Oper(label: str = None, order: int = 0, headOper: str = None, 
            isVisible: bool = True, icon: str = None, shortcut: str = None, 
            isCheckable: bool = False, tooltip: str = None):
    def decorator(func):
        func._type = OPER
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