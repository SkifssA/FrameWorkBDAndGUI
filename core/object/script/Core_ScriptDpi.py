# Системный файл для логики
import asyncio
from core.base import BaseApi, gid

class Core_ScriptObj:
    def __init__(self):
        self.id:int = None
        self.gid:gid = None
        self.sAction:str = None
        self.nVersion:int = None

class Core_ScriptDpi(BaseApi):
    _classObj = Core_ScriptObj

    async def _getNameClass(self):
        return "Core_Script"

    def calcHeadLine(self, rop:Core_ScriptObj)->str:
        return f'{rop.sAction}'

    def calcMnemoCode(self, rop:Core_ScriptObj)->str:
        return f'{rop.id}'

    async def insert(self)->Core_ScriptObj:
        return await super().insert()

    async def delete(self, rop:Core_ScriptObj)->None:
        
        return await super().delete(rop)
    
    async def update(self, rop:Core_ScriptObj)->None:
        return await super().update(rop)
    
    async def load(self, id: int)->Core_ScriptObj:
        return await super().load(id)
