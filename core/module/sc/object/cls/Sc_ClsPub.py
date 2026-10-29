# Пользовательский файл для интерфейса
from .Sc_ClsDvi import Sc_ClsDvi

class Sc_ClsPub(Sc_ClsDvi):

    metaFile = 'Sc_Cls.Ameta.json'

    class List(Sc_ClsDvi.DviList): pass

    class Card(Sc_ClsDvi.DviCard): pass

    class LookUp(Sc_ClsDvi.DviLookUp): pass

    @classmethod
    def list(cls, **kwargs): return cls.List(cls, **kwargs)

    @classmethod
    def card(cls, **kwargs): return cls.Card(cls, **kwargs)
