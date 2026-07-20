# Пользовательский файл для интерфейса
from .Awh_GenreDvi import Awh_GenreDvi
from engine.fabric.Form import FormConstruct

class Awh_GenreAvi(Awh_GenreDvi):
    class List(Awh_GenreDvi.DviList): pass

    class Card(Awh_GenreDvi.DviCard): pass

    class LookUp(Awh_GenreDvi.DviLookUp): pass

    @classmethod
    def list(cls)->FormConstruct:
        return FormConstruct(cls.List)
    
    @classmethod
    def card(cls)->FormConstruct:
        return FormConstruct(cls.Card)
