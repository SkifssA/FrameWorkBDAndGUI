# Пользовательский файл для интерфейса
from .Ir_ItemLootDvi import Ir_ItemLootDvi

class Ir_ItemLootAvi(Ir_ItemLootDvi):
    class List(Ir_ItemLootDvi.DviList): pass

    class Card(Ir_ItemLootDvi.DviCard): pass

    class LookUp(Ir_ItemLootDvi.DviLookUp): pass

    @classmethod
    def list(cls, **kwargs)->List:
        return cls.typeMeta(cls.List, **kwargs)
    
    @classmethod
    def card(cls, **kwargs)->Card:
        return cls.typeMeta(cls.Card, **kwargs)
