# Системный файл для логики
import asyncio
from engine.base import BaseApi, BaseObj, gid

class Gmb_TaskDetObj(BaseObj):
    def __init__(self):
        self.id:int = None
        self.gid:gid = None
        self.idTask:int = None
        self.idMod:int = None
        self.sIdMR:str = None
        self.sLastComment:str = None
        self.bMerged:int = None

class Gmb_TaskDetDpi(BaseApi):
    _classObj = Gmb_TaskDetObj

    def _getNameClass(self):
        return "Gmb_TaskDet"

    def calcHeadLine(self, rop:Gmb_TaskDetObj)->str:
        return f'{rop.id}'

    def calcMnemoCode(self, rop:Gmb_TaskDetObj)->str:
        return f'{rop.idTask} {rop.idMod}'

    def insert(self):
        return super().insert()

    def getByMnemocode(self, value)->Gmb_TaskDetObj|None:   
        return super().getByMnemocode(value)

    def delete(self, rop:Gmb_TaskDetObj)->None:
        
        return super().delete(rop)
    
    def update(self, rop:Gmb_TaskDetObj)->None:
        return super().update(rop)
    
    def load(self, id: int)->Gmb_TaskDetObj:
        return super().load(id)

    def setidTask(self, obj:Gmb_TaskDetObj, value): obj.idTask = value
    def setidMod(self, obj:Gmb_TaskDetObj, value): obj.idMod = value
    def setsIdMR(self, obj:Gmb_TaskDetObj, value): obj.sIdMR = value
    def setsLastComment(self, obj:Gmb_TaskDetObj, value): obj.sLastComment = value
    def setbMerged(self, obj:Gmb_TaskDetObj, value): obj.bMerged = value
