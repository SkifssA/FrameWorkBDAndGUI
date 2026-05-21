# Системный файл для логики
import asyncio
from engine.base import BaseApi, BaseObj, gid

class Hbc_StudentDataObj(BaseObj):
    def __init__(self):
        self.id:int = None
        self.gid:gid = None
        self.idStudent:int = None
        self.sData:str = None

class Hbc_StudentDataDpi(BaseApi):
    _classObj = Hbc_StudentDataObj

    def _getNameClass(self):
        return "Hbc_StudentData"

    def calcHeadLine(self, rop:Hbc_StudentDataObj)->str:
        return f'{rop.id}'

    def calcMnemoCode(self, rop:Hbc_StudentDataObj)->str:
        return f'{rop.id}'

    def insert(self)->Hbc_StudentDataObj:
        return super().insert()

    def getByMnemocode(self, value)->Hbc_StudentDataObj|None:   
        return super().getByMnemocode(value)

    def delete(self, rop:Hbc_StudentDataObj)->None:
        
        return super().delete(rop)
    
    def update(self, rop:Hbc_StudentDataObj)->None:
        return super().update(rop)
    
    def load(self, id: int)->Hbc_StudentDataObj:
        return super().load(id)

    def setidStudent(self, obj:Hbc_StudentDataObj, value): obj.idStudent = value
    def setsData(self, obj:Hbc_StudentDataObj, value): obj.sData = value
