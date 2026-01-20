# Пользовательский файл для логики
from .Bc_ScriptSchedulerDpi import Bc_ScriptSchedulerDpi, Bc_ScriptSchedulerObj

class Bc_ScriptSchedulerApi(Bc_ScriptSchedulerDpi):
    def setsNameScript(self, obj, value:str):
        super().setsNameScript(obj, value)
        if (value is not None):
            self.setsNameModule(obj, value[:value.find('_')].lower())

    def test(self):
        print("TEST из Bc_ScriptSchedulerApi")