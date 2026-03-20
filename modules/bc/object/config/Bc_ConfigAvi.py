# Пользовательский файл для интерфейса
from .Bc_ConfigDvi import Bc_ConfigDvi
from modules.bc.object.scriptscheduler.Bc_ScriptSchedulerAvi import Bc_ScriptSchedulerAvi

class Bc_ConfigAvi(Bc_ConfigDvi):
    @classmethod
    def list(cls, **kwargs):
        return cls.typeMeta(cls.List, **kwargs)
    
    @classmethod
    def card(cls, **kwargs):
        return cls.typeMeta(cls.Card, **kwargs)

    class List(Bc_ConfigDvi.DviList): 
        def openCh(self):
            yield Bc_ScriptSchedulerAvi.list()

    class Card(Bc_ConfigDvi.DviCard): pass

    class LookUp(Bc_ConfigDvi.DviLookUp): pass
