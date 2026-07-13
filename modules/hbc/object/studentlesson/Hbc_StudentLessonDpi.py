# Системный файл для логики
import asyncio
from engine.base import BaseApi, BaseObj, gid

class Hbc_StudentLessonObj(BaseObj):
    def __init__(self):
        self.id:int = None
        self.gid:gid = None
        self.idStudent:int = None
        self.idLesson:int = None
        self.bUploadFile:int = None
        self.bFillScore:int = None

class Hbc_StudentLessonDpi(BaseApi):
    _classObj = Hbc_StudentLessonObj

    def _getNameClass(self):
        return "Hbc_StudentLesson"

    def calcHeadLine(self, rop:Hbc_StudentLessonObj)->str:
        return f'{rop.id}'

    def calcMnemoCode(self, rop:Hbc_StudentLessonObj)->str:
        return f'{rop.idStudent} {rop.idLesson}'

    def insert(self)->Hbc_StudentLessonObj:
        return super().insert()

    def getByMnemocode(self, value)->Hbc_StudentLessonObj|None:   
        return super().getByMnemocode(value)

    def delete(self, rop:Hbc_StudentLessonObj)->None:
        from bc.object.file.Bc_FileApi import Bc_FileApi
        for i in Bc_FileApi()._getAllByAttr('gidScr', rop.gid):
            Bc_FileApi().delete(i)
        return super().delete(rop)
    
    def update(self, rop:Hbc_StudentLessonObj)->None:
        return super().update(rop)
    
    def load(self, id: int)->Hbc_StudentLessonObj:
        return super().load(id)

    def setidStudent(self, obj:Hbc_StudentLessonObj, value): obj.idStudent = value
    def setidLesson(self, obj:Hbc_StudentLessonObj, value): obj.idLesson = value
    def setbUploadFile(self, obj:Hbc_StudentLessonObj, value): obj.bUploadFile = value
    def setbFillScore(self, obj:Hbc_StudentLessonObj, value): obj.bFillScore = value
