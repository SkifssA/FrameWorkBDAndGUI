# Пользовательский файл для логики
from .Bc_ScriptSchedulerDpi import Bc_ScriptSchedulerDpi, Bc_ScriptSchedulerObj

class Bc_ScriptSchedulerApi(Bc_ScriptSchedulerDpi):
    async def register(self, sNameScript:str, sHour:str=None, sMinute:str=None, sSec:str=None, bRepeat:int=0, bUsed:int=1):
        obj = self.findByMnemocode(sNameScript)
        if obj is not None:
            obj = await super().insert()
            self.setsNameScript(obj, sNameScript)
        self.setnHour(obj, sHour)
        self.setnMinute(obj, sMinute)
        self.setnSec(obj, sSec)
        self.setbRepeat(obj, bRepeat)
        self.setbUsed(obj, bUsed)
        await self.update(obj)
    

    def setsNameScript(self, obj, value:str):
        super().setsNameScript(obj, value)
        if (value is not None):
            self.setsNameModule(obj, value[:value.find('_')].lower())

    def test(self):
        print("TEST из Bc_ScriptSchedulerApi")