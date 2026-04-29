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

    async def insert(self)->Hbc_StudentObj:
        return await super().insert()

    async def delete(self, rop:Hbc_StudentObj)->None:
        from ...object.studentdata.Hbc_StudentDataApi import Hbc_StudentDataApi
        d = await Hbc_StudentDataApi()._getAllByAttr('idStudent', rop.id)
        if d: asyncio.gather(*(Hbc_StudentDataApi().delete(i) for i in d))
        from ...object.studentlesson.Hbc_StudentLessonApi import Hbc_StudentLessonApi
        d = await Hbc_StudentLessonApi()._getAllByAttr('idStudent', rop.id)
        if d: asyncio.gather(*(Hbc_StudentLessonApi().delete(i) for i in d))
        return await super().delete(rop)
    
    async def update(self, rop:Hbc_StudentObj)->None:
        return await super().update(rop)
    
    def load(self, id: int)->Hbc_StudentObj:
        return super().load(id)

    def setsName(self, obj:Hbc_StudentObj, value): obj.sName = value
    def setsContact(self, obj:Hbc_StudentObj, value): obj.sContact = value
    def setsIpVM(self, obj:Hbc_StudentObj, value): obj.sIpVM = value
    def setsLoginVM(self, obj:Hbc_StudentObj, value): obj.sLoginVM = value
    def setsPassworVM(self, obj:Hbc_StudentObj, value): obj.sPassworVM = value
    def setsIdNew(self, obj:Hbc_StudentObj, value): obj.sIdNew = value
    def setbEnd(self, obj:Hbc_StudentObj, value): obj.bEnd = value
