# Пользовательский файл для интерфейса
from .Bc_ConfigDvi import Bc_ConfigDvi

class Bc_ConfigAvi(Bc_ConfigDvi):
    class EmptyCard(Bc_ConfigDvi.DviCard):
        def onRefresh(self):
            return ''

    class List(Bc_ConfigDvi.DviList): pass

    class Card(Bc_ConfigDvi.DviCard): pass

    class LookUp(Bc_ConfigDvi.DviLookUp): pass

    @classmethod
    def list(cls, **kwargs)->List:
        return cls.typeMeta(cls.List, **kwargs)
    
    @classmethod
    def emptyCard(cls, **kwargs)->EmptyCard:
        return cls.typeMeta(cls.EmptyCard, **kwargs)
    
    @classmethod
    def card(cls, **kwargs)->Card:
        return cls.typeMeta(cls.Card, **kwargs)
