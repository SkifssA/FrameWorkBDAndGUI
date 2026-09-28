# Системный файл для логики
from core.sdk import EmptyApi, EmptyObj

class Bc_TimeLineObj(EmptyObj):
    def __init__(self):
        self.id:int = None
        self.sCode:str = None
        self.sName:str = None

class Bc_TimeLineDpi(EmptyApi):
    _classObj = Bc_TimeLineObj

    def _getNameClass(self):
        return "Bc_TimeLine"

    def calcHeadLine(self, rop:Bc_TimeLineObj)->str:
        return f'{rop.sName}'

    def calcMnemoCode(self, rop:Bc_TimeLineObj)->str:
        return f'{rop.sCode}'

    def insert(self)->Bc_TimeLineObj:
        return super().insert()

    def getByMnemocode(self, value)->Bc_TimeLineObj|None:   
        return super().getByMnemocode(value)

    def delete(self, rop:Bc_TimeLineObj)->None:
        
        return super().delete(rop)
    
    def update(self, rop:Bc_TimeLineObj)->None:
        return super().update(rop)
    
    def load(self, id: int)->Bc_TimeLineObj:
        return super().load(id)

    def setsCode(self, obj:Bc_TimeLineObj, value): obj.sCode = value
    def setsName(self, obj:Bc_TimeLineObj, value): obj.sName = value
