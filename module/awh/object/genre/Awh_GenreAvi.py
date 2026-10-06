# Пользовательский файл для интерфейса
from .Awh_GenreDvi import Awh_GenreDvi

class Awh_GenreAvi(Awh_GenreDvi):
    class List(Awh_GenreDvi.DviList): pass

    class Card(Awh_GenreDvi.DviCard): pass

    class LookUp(Awh_GenreDvi.DviLookUp): pass
