# Системный файл для логики
from core.sdk import EmptyLogic, EmptyObj
from dataclasses import dataclass
from typing import Optional

@dataclass
class Bc_ScriptSchedulerObj(EmptyObj):
    id:int
    sNameScript:Optional[str] = None
    sNameModule:Optional[str] = None
    bRepeat:Optional[int] = None
    nTime:Optional[int] = None
    idTimeLine:Optional[int] = None
    bUsed:Optional[int] = None

class Bc_ScriptSchedulerDpi(EmptyLogic[Bc_ScriptSchedulerObj]):
    _classObj = Bc_ScriptSchedulerObj

    def _getNameClass(self):
        return "Bc_ScriptScheduler"

    def calcHeadLine(self, rop:Bc_ScriptSchedulerObj)->str:
        return f'{rop.id}'

    def calcMnemoCode(self, rop:Bc_ScriptSchedulerObj)->str:
        return f'{rop.sNameScript}'

    def setsNameScript(self, obj:Bc_ScriptSchedulerObj, value): obj.sNameScript = value
    def setsNameModule(self, obj:Bc_ScriptSchedulerObj, value): obj.sNameModule = value
    def setbRepeat(self, obj:Bc_ScriptSchedulerObj, value): obj.bRepeat = value
    def setnTime(self, obj:Bc_ScriptSchedulerObj, value): obj.nTime = value
    def setidTimeLine(self, obj:Bc_ScriptSchedulerObj, value): obj.idTimeLine = value
    def setbUsed(self, obj:Bc_ScriptSchedulerObj, value): obj.bUsed = value
