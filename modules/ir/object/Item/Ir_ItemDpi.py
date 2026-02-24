# Системный файл для логики
import asyncio
from core.base import BaseApi, BaseObj, gid

class Ir_ItemObj(BaseObj):
    def __init__(self):
        self.id:int = None
        self.gid:gid = None
        self.gidScr:gid = None

class Ir_ItemDpi(BaseApi):
    _classObj = Ir_ItemObj

    def _getNameClass(self):
        return "Ir_Item"

    def calcHeadLine(self, rop:Ir_ItemObj)->str:
        return f'{rop.id}'

    def calcMnemoCode(self, rop:Ir_ItemObj)->str:
        return f'{rop.id}'

    async def insert(self)->Ir_ItemObj:
        return await super().insert()

    async def delete(self, rop:Ir_ItemObj)->None:
        
        return await super().delete(rop)
    
    async def update(self, rop:Ir_ItemObj)->None:
        return await super().update(rop)
    
    async def load(self, id: int)->Ir_ItemObj:
        return await super().load(id)

    def setgidScr(self, obj:Ir_ItemObj, value): obj.gidScr = value
