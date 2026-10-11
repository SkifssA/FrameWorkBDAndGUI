# Пользовательский файл для интерфейса
from .Awh_GenreDvi import Awh_GenreDvi
from core.sdk import Form


class Awh_GenrePub(Awh_GenreDvi):
    metaFile = "Awh_Genre.Ameta.json"

    class List(Awh_GenreDvi.DviList):
        pass

    class Card(Awh_GenreDvi.DviCard):
        pass

    class LookUp(Awh_GenreDvi.DviLookUp):
        pass

    @classmethod
    def list(cls):
        return Form(cls.List, cls)

    @classmethod
    def card(cls):
        return Form(cls.Card, cls)
