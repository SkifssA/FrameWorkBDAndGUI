# Системный файл для логики
import asyncio
from core.base import BaseApi, BaseObj, gid

class Core_AttrObj(BaseObj):
    def __init__(self):
        self.id:int = None
        self.gid:gid = None
        self.idTab:int = None
        self.sCode:str = None
        self.sCaption:str = None
        self.sType:str = None
        self.sRefClass:str = None

class Core_AttrDpi(BaseApi):
    _classObj = Core_AttrObj

    def _getNameClass(self):
        return "Core_Attr"

    def calcHeadLine(self, rop:Core_AttrObj)->str:
        return f'{rop.idTab} {rop.sCaption} {rop.sType}'

    def calcMnemoCode(self, rop:Core_AttrObj)->str:
        return f'{rop.idTab} {rop.sCode}'

    async def insert(self)->Core_AttrObj:
        return await super().insert()

    async def delete(self, rop:Core_AttrObj)->None:
        
        return await super().delete(rop)
    
    async def update(self, rop:Core_AttrObj)->None:
        return await super().update(rop)
    
    async def load(self, id: int)->Core_AttrObj:
        return await super().load(id)

    def setidTab(self, obj:Core_AttrObj, value): obj.idTab = value
    def setsCode(self, obj:Core_AttrObj, value): obj.sCode = value
    def setsCaption(self, obj:Core_AttrObj, value): obj.sCaption = value
    def setsType(self, obj:Core_AttrObj, value): obj.sType = value
    def setsRefClass(self, obj:Core_AttrObj, value): obj.sRefClass = value
