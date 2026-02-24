# Системный файл для логики
import asyncio
from core.base import BaseApi, BaseObj, gid

class Ir_WeaponTypeObj(BaseObj):
    def __init__(self):
        self.id:int = None
        self.gid:gid = None
        self.sCaption:str = None
        self.sCode:str = None

class Ir_WeaponTypeDpi(BaseApi):
    _classObj = Ir_WeaponTypeObj

    def _getNameClass(self):
        return "Ir_WeaponType"

    def calcHeadLine(self, rop:Ir_WeaponTypeObj)->str:
        return f'{rop.sCaption}'

    def calcMnemoCode(self, rop:Ir_WeaponTypeObj)->str:
        return f'{rop.sCode}'

    async def insert(self)->Ir_WeaponTypeObj:
        return await super().insert()

    async def delete(self, rop:Ir_WeaponTypeObj)->None:
        
        return await super().delete(rop)
    
    async def update(self, rop:Ir_WeaponTypeObj)->None:
        return await super().update(rop)
    
    async def load(self, id: int)->Ir_WeaponTypeObj:
        return await super().load(id)

    def setsCaption(self, obj:Ir_WeaponTypeObj, value): obj.sCaption = value
    def setsCode(self, obj:Ir_WeaponTypeObj, value): obj.sCode = value
