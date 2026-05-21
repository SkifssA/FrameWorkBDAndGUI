# Системный файл для логики
import asyncio
from engine.base import BaseApi, BaseObj, gid

class Bc_FileObj(BaseObj):
    def __init__(self):
        self.id:int = None
        self.gid:gid = None
        self.gidScr:gid = None
        self.sCaption:str = None
        self.sSuffix:str = None
        self.sPath:str = None

class Bc_FileDpi(BaseApi):
    _classObj = Bc_FileObj

    def _getNameClass(self):
        return "Bc_File"

    def calcHeadLine(self, rop:Bc_FileObj)->str:
        return f'{rop.id}'

    def calcMnemoCode(self, rop:Bc_FileObj)->str:
        return f'{rop.id}'

    def insert(self)->Bc_FileObj:
        return super().insert()

    def getByMnemocode(self, value)->Bc_FileObj|None:   
        return super().getByMnemocode(value)

    def delete(self, rop:Bc_FileObj)->None:
        
        return super().delete(rop)
    
    def update(self, rop:Bc_FileObj)->None:
        return super().update(rop)
    
    def load(self, id: int)->Bc_FileObj:
        return super().load(id)

    def setgidScr(self, obj:Bc_FileObj, value): obj.gidScr = value
    def setsCaption(self, obj:Bc_FileObj, value): obj.sCaption = value
    def setsSuffix(self, obj:Bc_FileObj, value): obj.sSuffix = value
    def setsPath(self, obj:Bc_FileObj, value): obj.sPath = value
