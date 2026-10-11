# Пользовательский файл для интерфейса
from .Awh_AnimeGenreDvi import Awh_AnimeGenreDvi
from core.sdk import Form


class Awh_AnimeGenrePub(Awh_AnimeGenreDvi):
    metaFile = "Awh_AnimeGenre.Ameta.json"

    class List(Awh_AnimeGenreDvi.DviList):
        pass

    class Card(Awh_AnimeGenreDvi.DviCard):
        pass

    class LookUp(Awh_AnimeGenreDvi.DviLookUp):
        pass

    @classmethod
    def list(cls):
        return Form(cls.List, cls)

    @classmethod
    def card(cls):
        return Form(cls.Card, cls)
