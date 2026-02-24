# Пользовательский файл для интерфейса
from .Ir_DefDvi import Ir_DefDvi

class Ir_DefAvi(Ir_DefDvi):
    class List(Ir_DefDvi.DviList): pass

    class Card(Ir_DefDvi.DviCard): pass

    class LookUp(Ir_DefDvi.DviLookUp): pass

    @classmethod
    def list(cls, **kwargs)->List:
        return cls.typeMeta(cls.List, **kwargs)
    
    @classmethod
    def card(cls, **kwargs)->Card:
        return cls.typeMeta(cls.Card, **kwargs)
