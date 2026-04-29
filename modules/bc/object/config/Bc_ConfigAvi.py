# Пользовательский файл для интерфейса
from .Bc_ConfigDvi import Bc_ConfigDvi
from core.fabric.Form import FormConstruct

class Bc_ConfigAvi(Bc_ConfigDvi):
    class EmptyCard(Bc_ConfigDvi.DviCard):
        def onRefresh(self):
            return ''

    class List(Bc_ConfigDvi.DviList): pass

    class Card(Bc_ConfigDvi.DviCard): pass

    class LookUp(Bc_ConfigDvi.DviLookUp): pass

    @classmethod
    def list(cls)->FormConstruct:
        return FormConstruct(cls.List)
    
    @classmethod
    def emptyCard(cls)->FormConstruct:
        return FormConstruct(cls.EmptyCard)
    
    @classmethod
    def card(cls)->FormConstruct:
        return FormConstruct(cls.Card)
