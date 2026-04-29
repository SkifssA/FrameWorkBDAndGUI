# Системный файл для логики
import asyncio
from engine.base import BaseApi, BaseObj, gid

class Bc_IconsObj(BaseObj):
    def __init__(self):
        self.id:int = None
        self.gid:gid = None
        self.sCode:str = None
        self.sPath:str = None

class Bc_IconsDpi(BaseApi):
    _classObj = Bc_IconsObj

    def _getNameClass(self):
        return "Bc_Icons"

    def calcHeadLine(self, rop:Bc_IconsObj)->str:
        return f'{rop.id}'

    def calcMnemoCode(self, rop:Bc_IconsObj)->str:
        return f'{rop.sCode}'

    async def insert(self)->Bc_IconsObj:
        return await super().insert()

    async def delete(self, rop:Bc_IconsObj)->None:
        
        return await super().delete(rop)
    
    async def update(self, rop:Bc_IconsObj)->None:
        return await super().update(rop)
    
    def load(self, id: int)->Bc_IconsObj:
        return super().load(id)

    def setsCode(self, obj:Bc_IconsObj, value): obj.sCode = value
    def setsPath(self, obj:Bc_IconsObj, value): obj.sPath = value
