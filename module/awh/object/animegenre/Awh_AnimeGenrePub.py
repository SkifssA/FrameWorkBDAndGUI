# Пользовательский файл для интерфейса
from .Awh_AnimeGenreDvi import Awh_AnimeGenreDvi

class Awh_AnimeGenrePub(Awh_AnimeGenreDvi):
    class List(Awh_AnimeGenreDvi.DviList): pass

    class Card(Awh_AnimeGenreDvi.DviCard): pass

    class LookUp(Awh_AnimeGenreDvi.DviLookUp): pass
