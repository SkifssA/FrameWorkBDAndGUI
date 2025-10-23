# Системный файл для логики
import asyncio
from core.base import BaseApi, gid

class Bs_ConfigObj:
    def __init__(self):
        self.id:int = None
        self.gid:gid = None
        self.sModule:str = None
        self.sCaprionSetting:str = None
        self.sValue:str = None

class Bs_ConfigDpi(BaseApi):
    _idClass = 1
    _classObj = Bs_ConfigObj

    def calcHeadLine(self, rop:Bs_ConfigObj)->str:
        return f'{rop.id}'

    def calcMnemoCode(self, rop:Bs_ConfigObj)->str:
        return f'{rop.sModule} {rop.sCaprionSetting}'

    async def insert(self)->Bs_ConfigObj:
        return await super().insert()

    async def delete(self, rop:Bs_ConfigObj)->None:
        
        return await super().delete(rop)
    
    async def update(self, rop:Bs_ConfigObj)->None:
        return await super().update(rop)
    
    async def load(self, id: int)->Bs_ConfigObj:
        return await super().load(id)
