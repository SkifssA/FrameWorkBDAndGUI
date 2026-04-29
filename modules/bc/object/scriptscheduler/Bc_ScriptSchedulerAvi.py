# Пользовательский файл для интерфейса
from .Bc_ScriptSchedulerDvi import Bc_ScriptSchedulerDvi
from core.fabric.Form import FormConstruct

class Bc_ScriptSchedulerAvi(Bc_ScriptSchedulerDvi):
    class List(Bc_ScriptSchedulerDvi.DviList): pass

    class Card(Bc_ScriptSchedulerDvi.DviCard): pass

    class LookUp(Bc_ScriptSchedulerDvi.DviLookUp): pass

    @classmethod
    def list(cls) ->FormConstruct:
        return FormConstruct(cls.List)
    
    @classmethod
    def card(cls) -> FormConstruct:
        return FormConstruct(cls.Card)
