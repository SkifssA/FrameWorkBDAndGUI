# Системный файл для логики
import asyncio
from engine.base import BaseApi, BaseObj, gid

class Gmb_TaskObj(BaseObj):
    def __init__(self):
        self.id:int = None
        self.gid:gid = None
        self.nNumTask:int = None
        self.sCapTask:str = None
        self.sBranch:str = None

class Gmb_TaskDpi(BaseApi):
    _classObj = Gmb_TaskObj

    def _getNameClass(self):
        return "Gmb_Task"

    def calcHeadLine(self, rop:Gmb_TaskObj)->str:
        return f'{rop.id}'

    def calcMnemoCode(self, rop:Gmb_TaskObj)->str:
        return f'{rop.nNumTask} {rop.sCapTask}'

    def insert(self)->Gmb_TaskObj:
        return super().insert()

    def getByMnemocode(self, value)->Gmb_TaskObj|None:   
        return super().getByMnemocode(value)

    def delete(self, rop:Gmb_TaskObj)->None:
        
        return super().delete(rop)
    
    def update(self, rop:Gmb_TaskObj)->None:
        return super().update(rop)
    
    def load(self, id: int)->Gmb_TaskObj:
        return super().load(id)

    def setnNumTask(self, obj:Gmb_TaskObj, value): obj.nNumTask = value
    def setsCapTask(self, obj:Gmb_TaskObj, value):
        obj.sCapTask = value
    def setsBranch(self, obj:Gmb_TaskObj, value): obj.sBranch = value
