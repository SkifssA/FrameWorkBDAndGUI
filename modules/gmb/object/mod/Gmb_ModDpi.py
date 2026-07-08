# Системный файл для логики
import asyncio
from engine.base import BaseApi, BaseObj, gid

class Gmb_ModObj(BaseObj):
    def __init__(self):
        self.id:int = None
        self.gid:gid = None
        self.idTask:int = None
        self.sCapTask:str = None

class Gmb_ModDpi(BaseApi):
    _classObj = Gmb_ModObj

    def _getNameClass(self):
        return "Gmb_Mod"

    def calcHeadLine(self, rop:Gmb_ModObj)->str:
        return f'{rop.id}'

    def calcMnemoCode(self, rop:Gmb_ModObj)->str:
        return f'{rop.sCapTask}'

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

    def setidTask(self, obj:Gmb_ModObj, value): obj.idTask = value
    def setsCapTask(self, obj:Gmb_ModObj, value): obj.sCapTask = value
