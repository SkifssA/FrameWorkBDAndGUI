# Системный файл для логики
import asyncio
from core.base import BaseApi, BaseObj, gid

class Core_ClassObj(BaseObj):
    def __init__(self):
        self.id:int = None
        self.gid:gid = None
        self.sCode:str = None
        self.sCaption:str = None

class Core_ClassDpi(BaseApi):
    _classObj = Core_ClassObj

    def _getNameClass(self):
        return "Core_Class"

    def calcHeadLine(self, rop:Core_ClassObj)->str:
        return f'{rop.sCaption}'

    def calcMnemoCode(self, rop:Core_ClassObj)->str:
        return f'{rop.sCode}'

    async def insert(self)->Core_ClassObj:
        return await super().insert()

    async def delete(self, rop:Core_ClassObj)->None:
        from ...object.attr.Core_AttrApi import Core_AttrApi
        d = await Core_AttrApi()._getAllByAttr('idClass', rop.id)
        if d: asyncio.gather(*(Core_AttrApi().delete(i) for i in d))
        return await super().delete(rop)
    
    async def update(self, rop:Core_ClassObj)->None:
        return await super().update(rop)
    
    async def load(self, id: int)->Core_ClassObj:
        return await super().load(id)

    def setsCode(self, obj:Core_ClassObj, value): obj.sCode = value
    def setsCaption(self, obj:Core_ClassObj, value): obj.sCaption = value
