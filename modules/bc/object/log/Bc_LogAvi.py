# Пользовательский файл для интерфейса
from .Bc_LogDvi import Bc_LogDvi
from engine.fabric.Form import FormConstruct

class Bc_LogAvi(Bc_LogDvi):
    class List(Bc_LogDvi.DviList): pass

    class Card(Bc_LogDvi.DviCard): pass

    class LookUp(Bc_LogDvi.DviLookUp): pass

    @classmethod
    def list(cls)->FormConstruct:
        return FormConstruct(cls.List)
    
    @classmethod
    def card(cls)->FormConstruct:
        return FormConstruct(cls.Card)
