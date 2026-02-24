# Пользовательский файл для интерфейса
from .Ir_ItemDvi import Ir_ItemDvi

class Ir_ItemAvi(Ir_ItemDvi):
    class List(Ir_ItemDvi.DviList): pass

    class Card(Ir_ItemDvi.DviCard): pass

    class LookUp(Ir_ItemDvi.DviLookUp): pass

    @classmethod
    def list(cls, **kwargs)->List:
        return cls.typeMeta(cls.List, **kwargs)
    
    @classmethod
    def card(cls, **kwargs)->Card:
        return cls.typeMeta(cls.Card, **kwargs)
