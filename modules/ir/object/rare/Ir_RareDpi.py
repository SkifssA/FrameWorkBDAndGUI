# Системный файл для логики
import asyncio
from core.base import BaseApi, BaseObj, gid

class Ir_RareObj(BaseObj):
    def __init__(self):
        self.id:int = None
        self.gid:gid = None
        self.sCaption:str = None
        self.sCode:str = None
        self.sColor:str = None

class Ir_RareDpi(BaseApi):
    _classObj = Ir_RareObj

    def _getNameClass(self):
        return "Ir_Rare"

    def calcHeadLine(self, rop:Ir_RareObj)->str:
        return f'{rop.sCaption}'

    def calcMnemoCode(self, rop:Ir_RareObj)->str:
        return f'{rop.sCode}'

    async def insert(self)->Ir_RareObj:
        return await super().insert()

    async def delete(self, rop:Ir_RareObj)->None:
        
        return await super().delete(rop)
    
    async def update(self, rop:Ir_RareObj)->None:
        return await super().update(rop)
    
    async def load(self, id: int)->Ir_RareObj:
        return await super().load(id)

    def setsCaption(self, obj:Ir_RareObj, value): obj.sCaption = value
    def setsCode(self, obj:Ir_RareObj, value): obj.sCode = value
    def setsColor(self, obj:Ir_RareObj, value): obj.sColor = value
