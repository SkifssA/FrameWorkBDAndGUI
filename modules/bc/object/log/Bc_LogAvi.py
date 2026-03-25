# Пользовательский файл для интерфейса
from .Bc_LogDvi import Bc_LogDvi
from core.formhandle.FornManeger import FormHandle, FornManeger

class Bc_LogAvi(Bc_LogDvi):
    class List(Bc_LogDvi.DviList): pass

    class Card(Bc_LogDvi.DviCard): pass

    class LookUp(Bc_LogDvi.DviLookUp): pass

    @classmethod
    def list(cls)->FormHandle:
        return FornManeger.register(cls.List)
    
    @classmethod
    def card(cls)->FormHandle:
        return FornManeger.register(cls.Card)
