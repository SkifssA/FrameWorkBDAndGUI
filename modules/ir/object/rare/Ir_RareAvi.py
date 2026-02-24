# Пользовательский файл для интерфейса
from .Ir_RareDvi import Ir_RareDvi

class Ir_RareAvi(Ir_RareDvi):
    class List(Ir_RareDvi.DviList): pass

    class Card(Ir_RareDvi.DviCard): pass

    class LookUp(Ir_RareDvi.DviLookUp): pass

    @classmethod
    def list(cls, **kwargs)->List:
        return cls.typeMeta(cls.List, **kwargs)
    
    @classmethod
    def card(cls, **kwargs)->Card:
        return cls.typeMeta(cls.Card, **kwargs)
