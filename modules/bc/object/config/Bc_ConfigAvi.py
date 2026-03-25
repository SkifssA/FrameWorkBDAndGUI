# Пользовательский файл для интерфейса
from .Bc_ConfigDvi import Bc_ConfigDvi
from modules.bc.object.scriptscheduler.Bc_ScriptSchedulerAvi import Bc_ScriptSchedulerAvi
from core.formhandle.FornManeger import FormHandle, FornManeger

class Bc_ConfigAvi(Bc_ConfigDvi):
    class List(Bc_ConfigDvi.DviList): 
        def openCh(self):
            yield Bc_ScriptSchedulerAvi.list()

    class Card(Bc_ConfigDvi.DviCard): pass

    class LookUp(Bc_ConfigDvi.DviLookUp): pass

    @classmethod
    def list(cls)->FormHandle:
        return FornManeger.register(cls.List)
    
    @classmethod
    def card(cls)->FormHandle:
        return FornManeger.register(cls.Card)
