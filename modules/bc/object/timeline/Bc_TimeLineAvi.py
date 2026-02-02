# Пользовательский файл для интерфейса
from .Bc_TimeLineDvi import Bc_TimeLineDvi

class Bc_TimeLineAvi(Bc_TimeLineDvi):
    class List(Bc_TimeLineDvi.DviList): pass

    class Card(Bc_TimeLineDvi.DviCard): pass

    class LookUp(Bc_TimeLineDvi.DviLookUp): pass

    @classmethod
    def list(cls, **kwargs)->List:
        return cls.typeMeta(cls.List, **kwargs)
    
    @classmethod
    def card(cls, **kwargs)->Card:
        return cls.typeMeta(cls.Card, **kwargs)
