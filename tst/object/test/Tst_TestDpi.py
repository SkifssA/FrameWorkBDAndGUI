# Системный файл для логики
import asyncio
from core.base import BaseApi, BaseObj, gid

class Tst_TestObj(BaseObj):
    def __init__(self):
        self.id:int = None
        self.gid:gid = None
        self.sName:str = None
        self.nQty:int = None
        self.idConfig:int = None
        self.idConfigLook:int = None
        self.bEnd:int = None

class Tst_TestDpi(BaseApi):
    _classObj = Tst_TestObj

    def _getNameClass(self):
        return "Tst_Test"

    def calcHeadLine(self, rop:Tst_TestObj)->str:
        return f'{rop.sName}'

    def calcMnemoCode(self, rop:Tst_TestObj)->str:
        return f'{rop.id}'

    async def insert(self)->Tst_TestObj:
        return await super().insert()

    async def delete(self, rop:Tst_TestObj)->None:
        
        return await super().delete(rop)
    
    async def update(self, rop:Tst_TestObj)->None:
        return await super().update(rop)
    
    async def load(self, id: int)->Tst_TestObj:
        return await super().load(id)
