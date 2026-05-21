# Пользовательский файл для интерфейса
from .Core_ScriptDvi import Core_ScriptDvi
from engine.fabric.Form import FormConstruct

class Core_ScriptAvi(Core_ScriptDvi):
    class List(Core_ScriptDvi.DviList): pass

    class Card(Core_ScriptDvi.DviCard): pass

    class LookUp(Core_ScriptDvi.DviLookUp): pass

    @classmethod
    def list(cls)->FormConstruct:
        return FormConstruct(cls.List)
    
    @classmethod
    def card(cls)->FormConstruct:
        return FormConstruct(cls.Card)
