# Пользовательский файл для интерфейса
from .Awh_AnimeGenreDvi import Awh_AnimeGenreDvi

class Awh_AnimeGenreAvi(Awh_AnimeGenreDvi):
    class List(Awh_AnimeGenreDvi.DviList): pass

    class Card(Awh_AnimeGenreDvi.DviCard): pass

    class LookUp(Awh_AnimeGenreDvi.DviLookUp): pass

    @classmethod
    def list(cls, **kwargs)->List:
        return cls.typeMeta(cls.List, **kwargs)
    
    @classmethod
    def card(cls, **kwargs)->Card:
        return cls.typeMeta(cls.Card, **kwargs)
