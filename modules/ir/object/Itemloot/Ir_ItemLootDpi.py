# Системный файл для логики
import asyncio
from core.base import BaseApi, BaseObj, gid

class Ir_ItemLootObj(BaseObj):
    def __init__(self):
        self.id:int = None
        self.gid:gid = None
        self.sCaption:str = None
        self.idRare:int = None
        self.nScore:int = None

class Ir_ItemLootDpi(BaseApi):
    _classObj = Ir_ItemLootObj

    def _getNameClass(self):
        return "Ir_ItemLoot"

    def calcHeadLine(self, rop:Ir_ItemLootObj)->str:
        return f'{rop.sCaption}'

    def calcMnemoCode(self, rop:Ir_ItemLootObj)->str:
        return f'{rop.id}'

    async def insert(self)->Ir_ItemLootObj:
        return await super().insert()

    async def delete(self, rop:Ir_ItemLootObj)->None:
        
        return await super().delete(rop)
    
    async def update(self, rop:Ir_ItemLootObj)->None:
        return await super().update(rop)
    
    async def load(self, id: int)->Ir_ItemLootObj:
        return await super().load(id)

    def setsCaption(self, obj:Ir_ItemLootObj, value): obj.sCaption = value
    def setidRare(self, obj:Ir_ItemLootObj, value): obj.idRare = value
    def setnScore(self, obj:Ir_ItemLootObj, value): obj.nScore = value
