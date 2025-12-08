# Системный файл для логики
import asyncio
from core.base import BaseApi, BaseObj, gid

class Hbc_StudentDataObj(BaseObj):
    def __init__(self):
        self.id:int = None
        self.gid:gid = None
        self.idStudent:int = None
        self.sData:str = None

class Hbc_StudentDataDpi(BaseApi):
    _classObj = Hbc_StudentDataObj

    def _getNameClass(self):
        return "Hbc_StudentData"

    def calcHeadLine(self, rop:Hbc_StudentDataObj)->str:
        return f'{rop.id}'

    def calcMnemoCode(self, rop:Hbc_StudentDataObj)->str:
        return f'{rop.id}'

    async def insert(self)->Hbc_StudentDataObj:
        return await super().insert()

    async def delete(self, rop:Hbc_StudentDataObj)->None:
        
        return await super().delete(rop)
    
    async def update(self, rop:Hbc_StudentDataObj)->None:
        return await super().update(rop)
    
    async def load(self, id: int)->Hbc_StudentDataObj:
        return await super().load(id)
