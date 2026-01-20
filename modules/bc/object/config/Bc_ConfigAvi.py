# Пользовательский файл для интерфейса
from .Bc_ConfigDvi import Bc_ConfigDvi

class Bc_ConfigAvi(Bc_ConfigDvi):
    @classmethod
    def list(cls, **kwargs):
        return cls.typeMeta(cls.List, **kwargs)
    
    @classmethod
    def card(cls, **kwargs):
        return cls.typeMeta(cls.Card, **kwargs)

    class List(Bc_ConfigDvi.DviList): pass

    class Card(Bc_ConfigDvi.DviCard): pass

    class LookUp(Bc_ConfigDvi.DviLookUp): pass
