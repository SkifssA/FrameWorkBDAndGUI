# Системный файл для логики
import asyncio
from core.base import BaseApi, BaseObj, gid

class Hbc_LessonObj(BaseObj):
    def __init__(self):
        self.id:int = None
        self.gid:gid = None
        self.sCaption:str = None
        self.sIdExit:str = None

class Hbc_LessonDpi(BaseApi):
    _classObj = Hbc_LessonObj

    def _getNameClass(self):
        return "Hbc_Lesson"

    def calcHeadLine(self, rop:Hbc_LessonObj)->str:
        return f'{rop.sCaption}'

    def calcMnemoCode(self, rop:Hbc_LessonObj)->str:
        return f'{rop.id}'

    async def insert(self)->Hbc_LessonObj:
        return await super().insert()

    async def delete(self, rop:Hbc_LessonObj)->None:
        
        return await super().delete(rop)
    
    async def update(self, rop:Hbc_LessonObj)->None:
        return await super().update(rop)
    
    async def load(self, id: int)->Hbc_LessonObj:
        return await super().load(id)
