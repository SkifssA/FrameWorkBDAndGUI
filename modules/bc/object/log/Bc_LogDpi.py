# Системный файл для логики
import asyncio
from engine.base import BaseApi, BaseObj, gid

class Bc_LogObj(BaseObj):
    def __init__(self):
        self.id:int = None
        self.gid:gid = None
        self.sText:str = None

class Bc_LogDpi(BaseApi):
    _classObj = Bc_LogObj

    def _getNameClass(self):
        return "Bc_Log"

    def calcHeadLine(self, rop:Bc_LogObj)->str:
        return f'{rop.id}'

    def calcMnemoCode(self, rop:Bc_LogObj)->str:
        return f'{rop.id}'

    async def insert(self)->Bc_LogObj:
        return await super().insert()

    async def delete(self, rop:Bc_LogObj)->None:
        
        return await super().delete(rop)
    
    async def update(self, rop:Bc_LogObj)->None:
        return await super().update(rop)
    
    def load(self, id: int)->Bc_LogObj:
        return super().load(id)

    def setsText(self, obj:Bc_LogObj, value): obj.sText = value
