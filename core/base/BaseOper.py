import dearpygui.dearpygui as dpg

class Oper:
    def __init__(self, scen:str, op:str|list[str]):
        if isinstance(op, str):
            ops = [op]
        elif isinstance(op, list):
            ops = op
        else:
            raise TypeError("op должен быть str или list[str]")
        self.oper = tuple(f'{scen}_{i}' for i in ops)

    @property
    def isDisabled(self) -> bool:
        pass

    @isDisabled.setter
    def isDisabled(self, value):
        for i in self.oper:
            dpg.configure_item(i, enabled=not value)


def SetOper(label: str = None, order:int=0, headOper:str=None):
    def decorator(func):
        oper_id = func.__name__
        func._is_oper_handler = True
        func._oper_label = label or oper_id.replace('_', ' ').title()
        func._oper_id = oper_id
        func._order = order
        func._headOper = headOper
        func._is_long = False
        return func
    return decorator