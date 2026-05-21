# Системный файл для логики
import asyncio
from engine.base import BaseApi, BaseObj, gid

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

    def insert(self)->Hbc_LessonObj:
        return super().insert()

    def getByMnemocode(self, value)->Hbc_LessonObj|None:   
        return super().getByMnemocode(value)

    def delete(self, rop:Hbc_LessonObj)->None:
        
        return super().delete(rop)
    
    def update(self, rop:Hbc_LessonObj)->None:
        return super().update(rop)
    
    def load(self, id: int)->Hbc_LessonObj:
        return super().load(id)

    def setsCaption(self, obj:Hbc_LessonObj, value): obj.sCaption = value
    def setsIdExit(self, obj:Hbc_LessonObj, value): obj.sIdExit = value
