# Пользовательский файл для интерфейса
from .Bc_TimeLineDvi import Bc_TimeLineDvi
from core.formhandle.FornManeger import FormHandle, FornManeger

class Bc_TimeLineAvi(Bc_TimeLineDvi):
    class List(Bc_TimeLineDvi.DviList): pass

    class Card(Bc_TimeLineDvi.DviCard): pass

    class LookUp(Bc_TimeLineDvi.DviLookUp): pass

    @classmethod
    def list(cls)->FormHandle:
        return FornManeger.register(cls.List)
    
    @classmethod
    def card(cls)->FormHandle:
        return FornManeger.register(cls.Card)
