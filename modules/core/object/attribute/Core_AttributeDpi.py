# Системный файл для логики
import asyncio
from engine.base import BaseApi, BaseObj, gid

class Core_AttributeObj(BaseObj):
    def __init__(self):
        self.id:int = None
        self.gid:gid = None
        self.sCode:str = None
        self.sCaption:str = None
        self.idClass:int = None

class Core_AttributeDpi(BaseApi):
    _classObj = Core_AttributeObj

    def _getNameClass(self):
        return "Core_Attribute"

    def calcHeadLine(self, rop:Core_AttributeObj)->str:
        return f'{rop.sCaption}'

    def calcMnemoCode(self, rop:Core_AttributeObj)->str:
        return f'{rop.sCode}'

    async def insert(self)->Core_AttributeObj:
        return await super().insert()

    async def delete(self, rop:Core_AttributeObj)->None:
        
        return await super().delete(rop)
    
    async def update(self, rop:Core_AttributeObj)->None:
        return await super().update(rop)
    
    def load(self, id: int)->Core_AttributeObj:
        return super().load(id)

    def setsCode(self, obj:Core_AttributeObj, value): obj.sCode = value
    def setsCaption(self, obj:Core_AttributeObj, value): obj.sCaption = value
    def setidClass(self, obj:Core_AttributeObj, value): obj.idClass = value
