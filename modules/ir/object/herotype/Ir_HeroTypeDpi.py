# Системный файл для логики
import asyncio
from core.base import BaseApi, BaseObj, gid

class Ir_HeroTypeObj(BaseObj):
    def __init__(self):
        self.id:int = None
        self.gid:gid = None
        self.sCaption:str = None
        self.sCode:str = None
        self.idWeaponType:int = None
        self.idDefType:int = None

class Ir_HeroTypeDpi(BaseApi):
    _classObj = Ir_HeroTypeObj

    def _getNameClass(self):
        return "Ir_HeroType"

    def calcHeadLine(self, rop:Ir_HeroTypeObj)->str:
        return f'{rop.sCaption}'

    def calcMnemoCode(self, rop:Ir_HeroTypeObj)->str:
        return f'{rop.sCode}'

    async def insert(self)->Ir_HeroTypeObj:
        return await super().insert()

    async def delete(self, rop:Ir_HeroTypeObj)->None:
        
        return await super().delete(rop)
    
    async def update(self, rop:Ir_HeroTypeObj)->None:
        return await super().update(rop)
    
    async def load(self, id: int)->Ir_HeroTypeObj:
        return await super().load(id)

    def setsCaption(self, obj:Ir_HeroTypeObj, value): obj.sCaption = value
    def setsCode(self, obj:Ir_HeroTypeObj, value): obj.sCode = value
    def setidWeaponType(self, obj:Ir_HeroTypeObj, value): obj.idWeaponType = value
    def setidDefType(self, obj:Ir_HeroTypeObj, value): obj.idDefType = value
