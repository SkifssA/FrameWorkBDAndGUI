# Пользовательский файл для интерфейса
from .Awh_GenreDvi import Awh_GenreDvi

class Awh_GenreAvi(Awh_GenreDvi):
    @classmethod
    def list(cls, **kwargs):
        return cls.typeMeta(cls.List, **kwargs)
    
    @classmethod
    def card(cls, **kwargs):
        return cls.typeMeta(cls.Card, **kwargs)

    class List(Awh_GenreDvi.DviList): pass

    class Card(Awh_GenreDvi.DviCard): pass

    class LookUp(Awh_GenreDvi.DviLookUp): pass
