# Системный файл для логики
import asyncio
from core.base import BaseApi, BaseObj, gid

class Bc_ConfigObj(BaseObj):
    def __init__(self):
        self.id:int = None
        self.gid:gid = None
        self.sModule:str = None
        self.sCaprionSetting:str = None
        self.sValue:str = None

class Bc_ConfigDpi(BaseApi):
    _classObj = Bc_ConfigObj

    def _getNameClass(self):
        return "Bc_Config"

    def calcHeadLine(self, rop:Bc_ConfigObj)->str:
        return f'{rop.id}'

    def calcMnemoCode(self, rop:Bc_ConfigObj)->str:
        return f'{rop.sModule} {rop.sCaprionSetting}'

    async def insert(self)->Bc_ConfigObj:
        return await super().insert()

    async def delete(self, rop:Bc_ConfigObj)->None:
        
        return await super().delete(rop)
    
    async def update(self, rop:Bc_ConfigObj)->None:
        return await super().update(rop)
    
    async def load(self, id: int)->Bc_ConfigObj:
        return await super().load(id)
