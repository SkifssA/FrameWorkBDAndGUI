# Пользовательский файл для интерфейса
from .Awh_AnimeDvi import Awh_AnimeDvi
from core.sdk import Form

class Awh_AnimePub(Awh_AnimeDvi):

    metaFile = 'Awh_Anime.Ameta.json'

    class List(Awh_AnimeDvi.DviList): pass

    class Card(Awh_AnimeDvi.DviCard): pass

    class LookUp(Awh_AnimeDvi.DviLookUp): pass

    @classmethod
    def list(cls): return Form(cls.List, cls)

    @classmethod
    def card(cls): return Form(cls.Card, cls)
