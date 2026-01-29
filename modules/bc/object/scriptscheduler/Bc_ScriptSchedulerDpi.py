# Системный файл для логики
import asyncio
from core.base import BaseApi, BaseObj, gid

class Bc_ScriptSchedulerObj(BaseObj):
    def __init__(self):
        self.id:int = None
        self.gid:gid = None
        self.sNameScript:str = None
        self.sNameModule:str = None
        self.bRepeat:int = None
        self.nHour:int = None
        self.nMinute:int = None
        self.nSec:int = None
        self.bUsed:int = None

class Bc_ScriptSchedulerDpi(BaseApi):
    _classObj = Bc_ScriptSchedulerObj

    def _getNameClass(self):
        return "Bc_ScriptScheduler"

    def calcHeadLine(self, rop:Bc_ScriptSchedulerObj)->str:
        return f'{rop.id}'

    def calcMnemoCode(self, rop:Bc_ScriptSchedulerObj)->str:
        return f'{rop.sNameScript}'

    async def insert(self)->Bc_ScriptSchedulerObj:
        return await super().insert()

    async def delete(self, rop:Bc_ScriptSchedulerObj)->None:
        
        return await super().delete(rop)
    
    async def update(self, rop:Bc_ScriptSchedulerObj)->None:
        return await super().update(rop)
    
    async def load(self, id: int)->Bc_ScriptSchedulerObj:
        return await super().load(id)

    def setsNameScript(self, obj:Bc_ScriptSchedulerObj, value): obj.sNameScript = value
    def setsNameModule(self, obj:Bc_ScriptSchedulerObj, value): obj.sNameModule = value
    def setbRepeat(self, obj:Bc_ScriptSchedulerObj, value): obj.bRepeat = value
    def setnHour(self, obj:Bc_ScriptSchedulerObj, value): obj.nHour = value
    def setnMinute(self, obj:Bc_ScriptSchedulerObj, value): obj.nMinute = value
    def setnSec(self, obj:Bc_ScriptSchedulerObj, value): obj.nSec = value
    def setbUsed(self, obj:Bc_ScriptSchedulerObj, value): obj.bUsed = value
