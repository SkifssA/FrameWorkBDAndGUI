# Пользовательский файл для интерфейса
from .Sc_ScriptsDvi import Sc_ScriptsDvi

class Sc_ScriptsPub(Sc_ScriptsDvi):

    metaFile = 'Sc_Scripts.Ameta.json'

    class List(Sc_ScriptsDvi.DviList): pass

    class Card(Sc_ScriptsDvi.DviCard): pass

    class LookUp(Sc_ScriptsDvi.DviLookUp): pass

    @classmethod
    def list(cls, **kwargs): return cls.List(cls, **kwargs)

    @classmethod
    def card(cls, **kwargs): return cls.Card(cls, **kwargs)
