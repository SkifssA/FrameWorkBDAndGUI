# Пользовательский файл для интерфейса
from .Ir_HeroTypeDvi import Ir_HeroTypeDvi

class Ir_HeroTypeAvi(Ir_HeroTypeDvi):
    class List(Ir_HeroTypeDvi.DviList): pass

    class Card(Ir_HeroTypeDvi.DviCard): pass

    class LookUp(Ir_HeroTypeDvi.DviLookUp): pass

    @classmethod
    def list(cls, **kwargs)->List:
        return cls.typeMeta(cls.List, **kwargs)
    
    @classmethod
    def card(cls, **kwargs)->Card:
        return cls.typeMeta(cls.Card, **kwargs)
