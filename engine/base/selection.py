from .oper import Oper


class Selection:
    class Oper(Oper): pass

    def __init__(self, nameCls):
        self.nameCls = nameCls

    def oper(self, op:str|list[str])->Oper:
        return self.Oper(self.nameCls, op)
    
    def findSelection(self, aviSelection):
        from ..form.Base import Base
        return Base.getAllForm().get(str(aviSelection.__class__), None)