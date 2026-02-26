# Пользовательский файл для интерфейса
from .Bc_LogDvi import Bc_LogDvi

class Bc_LogAvi(Bc_LogDvi):
    class List(Bc_LogDvi.DviList): pass

    class Card(Bc_LogDvi.DviCard): pass

    class LookUp(Bc_LogDvi.DviLookUp): pass

    @classmethod
    def list(cls, **kwargs)->List:
        return cls.typeMeta(cls.List, **kwargs)
    
    @classmethod
    def card(cls, **kwargs)->Card:
        return cls.typeMeta(cls.Card, **kwargs)
