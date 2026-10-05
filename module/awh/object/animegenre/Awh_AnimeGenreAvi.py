# Пользовательский файл для интерфейса
from .Awh_AnimeGenreDvi import Awh_AnimeGenreDvi
from engineQT.sdk import FormConstruct

class Awh_AnimeGenreAvi(Awh_AnimeGenreDvi):
    class List(Awh_AnimeGenreDvi.DviList): pass

    class Card(Awh_AnimeGenreDvi.DviCard): pass

    @classmethod
    def list(cls)->FormConstruct:
        return FormConstruct(cls.List)
    
    @classmethod
    def card(cls)->FormConstruct:
        return FormConstruct(cls.Card)
