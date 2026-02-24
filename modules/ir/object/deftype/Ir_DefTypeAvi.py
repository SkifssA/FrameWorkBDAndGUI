# Пользовательский файл для интерфейса
from .Ir_DefTypeDvi import Ir_DefTypeDvi

class Ir_DefTypeAvi(Ir_DefTypeDvi):
    class List(Ir_DefTypeDvi.DviList): pass

    class Card(Ir_DefTypeDvi.DviCard): pass

    class LookUp(Ir_DefTypeDvi.DviLookUp): pass

    @classmethod
    def list(cls, **kwargs)->List:
        return cls.typeMeta(cls.List, **kwargs)
    
    @classmethod
    def card(cls, **kwargs)->Card:
        return cls.typeMeta(cls.Card, **kwargs)
