# Пользовательский файл для интерфейса
from .Awh_GenreDvi import Awh_GenreDvi

from core.formhandle.FornManeger import FormHandle, FornManeger

class Awh_GenreAvi(Awh_GenreDvi):
    class List(Awh_GenreDvi.DviList): pass

    class Card(Awh_GenreDvi.DviCard): pass

    class LookUp(Awh_GenreDvi.DviLookUp): pass

    @classmethod
    def list(cls)->FormHandle:
        return FornManeger.register(cls.List)
    
    @classmethod
    def card(cls)->FormHandle:
        return FornManeger.register(cls.Card)
