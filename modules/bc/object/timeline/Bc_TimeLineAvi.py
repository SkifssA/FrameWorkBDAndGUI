# Пользовательский файл для интерфейса
from .Bc_TimeLineDvi import Bc_TimeLineDvi
from core.fabric.Form import FormConstruct

class Bc_TimeLineAvi(Bc_TimeLineDvi):
    class List(Bc_TimeLineDvi.DviList): pass

    class Card(Bc_TimeLineDvi.DviCard): pass

    class LookUp(Bc_TimeLineDvi.DviLookUp): pass

    @classmethod
    def list(cls)->FormConstruct:
        return FormConstruct(cls.List)
    
    @classmethod
    def card(cls)->FormConstruct:
        return FormConstruct(cls.Card)
