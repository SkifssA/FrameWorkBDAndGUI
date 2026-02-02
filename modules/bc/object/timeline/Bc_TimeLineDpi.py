# Системный файл для логики
import asyncio
from core.base import BaseApi, BaseObj, gid

class Bc_TimeLineObj(BaseObj):
    def __init__(self):
        self.id:int = None
        self.gid:gid = None
        self.sCode:str = None
        self.sName:str = None

class Bc_TimeLineDpi(BaseApi):
    _classObj = Bc_TimeLineObj

    def _getNameClass(self):
        return "Bc_TimeLine"

    def calcHeadLine(self, rop:Bc_TimeLineObj)->str:
        return f'{rop.sName}'

    def calcMnemoCode(self, rop:Bc_TimeLineObj)->str:
        return f'{rop.sCode}'

    async def insert(self)->Bc_TimeLineObj:
        return await super().insert()

    async def delete(self, rop:Bc_TimeLineObj)->None:
        
        return await super().delete(rop)
    
    async def update(self, rop:Bc_TimeLineObj)->None:
        return await super().update(rop)
    
    async def load(self, id: int)->Bc_TimeLineObj:
        return await super().load(id)

    def setsCode(self, obj:Bc_TimeLineObj, value): obj.sCode = value
    def setsName(self, obj:Bc_TimeLineObj, value): obj.sName = value
