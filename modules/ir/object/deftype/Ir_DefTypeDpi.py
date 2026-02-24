# Системный файл для логики
import asyncio
from core.base import BaseApi, BaseObj, gid

class Ir_DefTypeObj(BaseObj):
    def __init__(self):
        self.id:int = None
        self.gid:gid = None
        self.sCaption:str = None
        self.sCode:str = None

class Ir_DefTypeDpi(BaseApi):
    _classObj = Ir_DefTypeObj

    def _getNameClass(self):
        return "Ir_DefType"

    def calcHeadLine(self, rop:Ir_DefTypeObj)->str:
        return f'{rop.sCaption}'

    def calcMnemoCode(self, rop:Ir_DefTypeObj)->str:
        return f'{rop.sCode}'

    async def insert(self)->Ir_DefTypeObj:
        return await super().insert()

    async def delete(self, rop:Ir_DefTypeObj)->None:
        
        return await super().delete(rop)
    
    async def update(self, rop:Ir_DefTypeObj)->None:
        return await super().update(rop)
    
    async def load(self, id: int)->Ir_DefTypeObj:
        return await super().load(id)

    def setsCaption(self, obj:Ir_DefTypeObj, value): obj.sCaption = value
    def setsCode(self, obj:Ir_DefTypeObj, value): obj.sCode = value
