# Пользовательский файл для интерфейса
from .Ir_HeroDvi import Ir_HeroDvi

class Ir_HeroAvi(Ir_HeroDvi):
    class List(Ir_HeroDvi.DviList): pass

    class Card(Ir_HeroDvi.DviCard): pass

    class LookUp(Ir_HeroDvi.DviLookUp): pass

    @classmethod
    def list(cls, **kwargs)->List:
        return cls.typeMeta(cls.List, **kwargs)
    
    @classmethod
    def card(cls, **kwargs)->Card:
        return cls.typeMeta(cls.Card, **kwargs)
