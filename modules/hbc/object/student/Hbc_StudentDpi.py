# Системный файл для логики
import asyncio
from engine.base import BaseApi, BaseObj, gid

class Hbc_StudentObj(BaseObj):
    def __init__(self):
        self.id:int = None
        self.gid:gid = None
        self.sName:str = None
        self.sContact:str = None
        self.sIpVM:str = None
        self.sLoginVM:str = None
        self.sPassworVM:str = None
        self.sIdNew:str = None
        self.bEnd:int = None

class Hbc_StudentDpi(BaseApi):
    _classObj = Hbc_StudentObj

    def _getNameClass(self):
        return "Hbc_Student"

    def calcHeadLine(self, rop:Hbc_StudentObj)->str:
        return f'{rop.sName}'

    def calcMnemoCode(self, rop:Hbc_StudentObj)->str:
        return f'{rop.id}'

    def insert(self)->Hbc_StudentObj:
        return super().insert()

    def getByMnemocode(self, value)->Hbc_StudentObj|None:   
        return super().getByMnemocode(value)

    def delete(self, rop:Hbc_StudentObj)->None:
        from ...object.studentdata.Hbc_StudentDataApi import Hbc_StudentDataApi
        for i in Hbc_StudentDataApi()._getAllByAttr('idStudent', rop.id):
            Hbc_StudentDataApi().delete(i)
        from ...object.studentlesson.Hbc_StudentLessonApi import Hbc_StudentLessonApi
        for i in Hbc_StudentLessonApi()._getAllByAttr('idStudent', rop.id):
            Hbc_StudentLessonApi().delete(i)
        return super().delete(rop)
    
    def update(self, rop:Hbc_StudentObj)->None:
        return super().update(rop)
    
    def load(self, id: int)->Hbc_StudentObj:
        return super().load(id)

    def setsName(self, obj:Hbc_StudentObj, value): obj.sName = value
    def setsContact(self, obj:Hbc_StudentObj, value): obj.sContact = value
    def setsIpVM(self, obj:Hbc_StudentObj, value): obj.sIpVM = value
    def setsLoginVM(self, obj:Hbc_StudentObj, value): obj.sLoginVM = value
    def setsPassworVM(self, obj:Hbc_StudentObj, value): obj.sPassworVM = value
    def setsIdNew(self, obj:Hbc_StudentObj, value): obj.sIdNew = value
    def setbEnd(self, obj:Hbc_StudentObj, value): obj.bEnd = value
