# Пользовательский файл для интерфейса
from .Awh_AnimeDvi import Awh_AnimeDvi

class Awh_AnimePub(Awh_AnimeDvi):
    class List(Awh_AnimeDvi.DviList): pass

    class Card(Awh_AnimeDvi.DviCard): pass

    class LookUp(Awh_AnimeDvi.DviLookUp): pass
