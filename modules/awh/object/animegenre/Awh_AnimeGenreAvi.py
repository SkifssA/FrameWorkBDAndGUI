# Пользовательский файл для интерфейса
from .Awh_AnimeGenreDvi import Awh_AnimeGenreDvi

from core.formhandle.FornManeger import FormHandle, FornManeger

class Awh_AnimeGenreAvi(Awh_AnimeGenreDvi):
    class List(Awh_AnimeGenreDvi.DviList): pass

    class Card(Awh_AnimeGenreDvi.DviCard): pass

    class LookUp(Awh_AnimeGenreDvi.DviLookUp): pass

    @classmethod
    def list(cls)->FormHandle:
        return FornManeger.register(cls.List)
    
    @classmethod
    def card(cls)->FormHandle:
        return FornManeger.register(cls.Card)
