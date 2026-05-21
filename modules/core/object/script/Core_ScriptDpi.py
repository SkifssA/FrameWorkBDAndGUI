# Системный файл для логики
import asyncio
from engine.base import BaseApi, BaseObj, gid

class Core_ScriptObj(BaseObj):
    def __init__(self):
        self.id:int = None
        self.gid:gid = None
        self.sCode:str = None
        self.nVersion:int = None

class Core_ScriptDpi(BaseApi):
    _classObj = Core_ScriptObj

    def _getNameClass(self):
        return "Core_Script"

    def calcHeadLine(self, rop:Core_ScriptObj)->str:
        return f'{rop.id}'

    def calcMnemoCode(self, rop:Core_ScriptObj)->str:
        return f'{rop.sCode}'

    def insert(self)->Core_ScriptObj:
        return super().insert()

    def getByMnemocode(self, value)->Core_ScriptObj|None:   
        return super().getByMnemocode(value)

    def delete(self, rop:Core_ScriptObj)->None:
        
        return super().delete(rop)
    
    def update(self, rop:Core_ScriptObj)->None:
        return super().update(rop)
    
    def load(self, id: int)->Core_ScriptObj:
        return super().load(id)

    def setsCode(self, obj:Core_ScriptObj, value): obj.sCode = value
    def setnVersion(self, obj:Core_ScriptObj, value): obj.nVersion = value
