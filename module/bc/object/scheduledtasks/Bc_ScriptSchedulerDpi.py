# Системный файл для логики
from core.sdk import EmptyApi, EmptyObj

class Bc_ScriptSchedulerObj(EmptyObj):
    def __init__(self):
        self.id:int = None
        self.sNameScript:str = None
        self.sNameModule:str = None
        self.bRepeat:int = None
        self.nTime:int = None
        self.idTimeLine:int = None
        self.bUsed:int = None

class Bc_ScriptSchedulerDpi(EmptyApi):
    _classObj = Bc_ScriptSchedulerObj

    def _getNameClass(self):
        return "Bc_ScriptScheduler"

    def calcHeadLine(self, rop:Bc_ScriptSchedulerObj)->str:
        return f'{rop.id}'

    def calcMnemoCode(self, rop:Bc_ScriptSchedulerObj)->str:
        return f'{rop.sNameScript}'

    def insert(self)->Bc_ScriptSchedulerObj:
        return super().insert()

    def getByMnemocode(self, value)->Bc_ScriptSchedulerObj|None:   
        return super().getByMnemocode(value)

    def delete(self, rop:Bc_ScriptSchedulerObj)->None:
        
        return super().delete(rop)
    
    def update(self, rop:Bc_ScriptSchedulerObj)->None:
        return super().update(rop)
    
    def load(self, id: int)->Bc_ScriptSchedulerObj:
        return super().load(id)

    def setsNameScript(self, obj:Bc_ScriptSchedulerObj, value): obj.sNameScript = value
    def setsNameModule(self, obj:Bc_ScriptSchedulerObj, value): obj.sNameModule = value
    def setbRepeat(self, obj:Bc_ScriptSchedulerObj, value): obj.bRepeat = value
    def setnTime(self, obj:Bc_ScriptSchedulerObj, value): obj.nTime = value
    def setidTimeLine(self, obj:Bc_ScriptSchedulerObj, value): obj.idTimeLine = value
    def setbUsed(self, obj:Bc_ScriptSchedulerObj, value): obj.bUsed = value
