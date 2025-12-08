# Системный файл для логики
import asyncio
from core.base import BaseApi, BaseObj, gid

class Tst_TestLookUpObj(BaseObj):
    def __init__(self):
        self.id:int = None
        self.gid:gid = None
        self.sName:str = None

class Tst_TestLookUpDpi(BaseApi):
    _classObj = Tst_TestLookUpObj

    def _getNameClass(self):
        return "Tst_TestLookUp"

    def calcHeadLine(self, rop:Tst_TestLookUpObj)->str:
        return f'{rop.sName}'

    def calcMnemoCode(self, rop:Tst_TestLookUpObj)->str:
        return f'{rop.id}'

    async def insert(self)->Tst_TestLookUpObj:
        return await super().insert()

    async def delete(self, rop:Tst_TestLookUpObj)->None:
        
        return await super().delete(rop)
    
    async def update(self, rop:Tst_TestLookUpObj)->None:
        return await super().update(rop)
    
    async def load(self, id: int)->Tst_TestLookUpObj:
        return await super().load(id)

    def setsName(self, obj:Tst_TestLookUpObj, value): obj.sName = value
