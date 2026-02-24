# Пользовательский файл для интерфейса
from .Ir_DefaDvi import Ir_DefaDvi

class Ir_DefaAvi(Ir_DefaDvi):
    class List(Ir_DefaDvi.DviList): pass

    class Card(Ir_DefaDvi.DviCard): pass

    class LookUp(Ir_DefaDvi.DviLookUp): pass

    @classmethod
    def list(cls, **kwargs)->List:
        return cls.typeMeta(cls.List, **kwargs)
    
    @classmethod
    def card(cls, **kwargs)->Card:
        return cls.typeMeta(cls.Card, **kwargs)
