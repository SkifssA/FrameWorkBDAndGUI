# Пользовательский файл для интерфейса
from .Bc_ScriptSchedulerDvi import Bc_ScriptSchedulerDvi
from core.formhandle.FornManeger import FormHandle, FornManeger

class Bc_ScriptSchedulerAvi(Bc_ScriptSchedulerDvi):
    class List(Bc_ScriptSchedulerDvi.DviList): pass

    class Card(Bc_ScriptSchedulerDvi.DviCard): pass

    class LookUp(Bc_ScriptSchedulerDvi.DviLookUp): pass

    @classmethod
    def list(cls)->FormHandle:
        return FornManeger.register(cls.List)
    
    @classmethod
    def card(cls)->FormHandle:
        return FornManeger.register(cls.Card)
