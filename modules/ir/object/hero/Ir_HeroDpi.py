# Системный файл для логики
import asyncio
from core.base import BaseApi, BaseObj, gid

class Ir_HeroObj(BaseObj):
    def __init__(self):
        self.id:int = None
        self.gid:gid = None
        self.sCaption:str = None
        self.nHead:int = None
        self.nHeadMax:int = None
        self.nStrong:int = None
        self.nMind:int = None
        self.nDexterit:int = None
        self.idType:int = None

class Ir_HeroDpi(BaseApi):
    _classObj = Ir_HeroObj

    def _getNameClass(self):
        return "Ir_Hero"

    def calcHeadLine(self, rop:Ir_HeroObj)->str:
        return f'{rop.sCaption}'

    def calcMnemoCode(self, rop:Ir_HeroObj)->str:
        return f'{rop.id}'

    async def insert(self)->Ir_HeroObj:
        return await super().insert()

    async def delete(self, rop:Ir_HeroObj)->None:
        
        return await super().delete(rop)
    
    async def update(self, rop:Ir_HeroObj)->None:
        return await super().update(rop)
    
    async def load(self, id: int)->Ir_HeroObj:
        return await super().load(id)

    def setsCaption(self, obj:Ir_HeroObj, value): obj.sCaption = value
    def setnHead(self, obj:Ir_HeroObj, value): obj.nHead = value
    def setnHeadMax(self, obj:Ir_HeroObj, value): obj.nHeadMax = value
    def setnStrong(self, obj:Ir_HeroObj, value): obj.nStrong = value
    def setnMind(self, obj:Ir_HeroObj, value): obj.nMind = value
    def setnDexterit(self, obj:Ir_HeroObj, value): obj.nDexterit = value
    def setidType(self, obj:Ir_HeroObj, value): obj.idType = value
