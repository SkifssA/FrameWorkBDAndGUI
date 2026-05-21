# Пользовательский файл для логики
from .Bc_ScriptSchedulerDpi import Bc_ScriptSchedulerDpi, Bc_ScriptSchedulerObj

class Bc_ScriptSchedulerApi(Bc_ScriptSchedulerDpi):
    def register(self, sNameScript:str, nTime:str=None, idTimeLine:str=None, bRepeat:int=0, bUsed:int=1):
        if not (obj:=self.getByMnemocode(sNameScript)):
            obj = super().insert()
            self.setsNameScript(obj, sNameScript)
        self.setnTime(obj, nTime)
        self.setidTimeLine(obj, idTimeLine)
        self.setbRepeat(obj, bRepeat)
        self.setbUsed(obj, bUsed)
        self.update(obj)
    

    def setsNameScript(self, obj, value:str):
        super().setsNameScript(obj, value)
        if (value is not None):
            self.setsNameModule(obj, value[:value.find('_')].lower())

    def test(self):
        print("TEST из Bc_ScriptSchedulerApi")