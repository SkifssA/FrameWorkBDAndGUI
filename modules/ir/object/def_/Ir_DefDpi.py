# Системный файл для логики
import asyncio
from core.base import BaseApi, BaseObj, gid

class Ir_DefObj(BaseObj):
    def __init__(self):
        self.id:int = None
        self.gid:gid = None
        self.sCaption:str = None
        self.idType:int = None
        self.idRare:int = None
        self.nScore:int = None

class Ir_DefDpi(BaseApi):
    _classObj = Ir_DefObj

    def _getNameClass(self):
        return "Ir_Def"

    def calcHeadLine(self, rop:Ir_DefObj)->str:
        return f'{rop.sCaption}'

    def calcMnemoCode(self, rop:Ir_DefObj)->str:
        return f'{rop.id}'

    async def insert(self)->Ir_DefObj:
        return await super().insert()

    async def delete(self, rop:Ir_DefObj)->None:
        
        return await super().delete(rop)
    
    async def update(self, rop:Ir_DefObj)->None:
        return await super().update(rop)
    
    async def load(self, id: int)->Ir_DefObj:
        return await super().load(id)

    def setsCaption(self, obj:Ir_DefObj, value): obj.sCaption = value
    def setidType(self, obj:Ir_DefObj, value): obj.idType = value
    def setidRare(self, obj:Ir_DefObj, value): obj.idRare = value
    def setnScore(self, obj:Ir_DefObj, value): obj.nScore = value
