# Системный файл для логики
import asyncio
from engine.base import BaseApi, BaseObj, gid

class Gmb_ModObj(BaseObj):
    def __init__(self):
        self.id:int = None
        self.gid:gid = None
        self.sCaption:str = None
        self.sReviewer:str = None
        self.sIdGitReviewer:str = None

class Gmb_ModDpi(BaseApi):
    _classObj = Gmb_ModObj

    def _getNameClass(self):
        return "Gmb_Mod"

    def calcHeadLine(self, rop:Gmb_ModObj)->str:
        return f'{rop.sCaption}'

    def calcMnemoCode(self, rop:Gmb_ModObj)->str:
        return f'{rop.sCaption}'

    def insert(self)->Gmb_ModObj:
        return super().insert()

    def getByMnemocode(self, value)->Gmb_ModObj|None:   
        return super().getByMnemocode(value)

    def delete(self, rop:Gmb_ModObj)->None:
        
        return super().delete(rop)
    
    def update(self, rop:Gmb_ModObj)->None:
        return super().update(rop)
    
    def load(self, id: int)->Gmb_ModObj:
        return super().load(id)

    def setsCaption(self, obj:Gmb_ModObj, value): obj.sCaption = value
    def setsReviewer(self, obj:Gmb_ModObj, value): obj.sReviewer = value
    def setsIdGitReviewer(self, obj:Gmb_ModObj, value): obj.sIdGitReviewer = value
