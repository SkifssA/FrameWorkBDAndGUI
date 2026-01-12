# Пользовательский файл для интерфейса
from .Awh_AnimeDvi import Awh_AnimeDvi

class Awh_AnimeAvi(Awh_AnimeDvi):
    @classmethod
    def list(cls, **kwargs):
        return cls.typeMeta(cls.List, **kwargs)
    
    @classmethod
    def card(cls, **kwargs):
        return cls.typeMeta(cls.Card, **kwargs)

    class List(Awh_AnimeDvi.DviList): pass

    class Card(Awh_AnimeDvi.DviCard): pass

    class LookUp(Awh_AnimeDvi.DviLookUp): pass
