# Пользовательский файл для интерфейса
from core.base.BaseOper import SetOper
from .Awh_AnimeDvi import Awh_AnimeDvi

from ..Awh_AnimeLoadPkg import Awh_AnimeLoadPkg

class Awh_AnimeAvi(Awh_AnimeDvi):
    @classmethod
    def list(cls, **kwargs):
        return cls.typeMeta(cls.List, **kwargs)
    
    @classmethod
    def card(cls, **kwargs):
        return cls.typeMeta(cls.Card, **kwargs)

    class List(Awh_AnimeDvi.DviList):
        @SetOper(label='Тест загрузки данных')
        async def uploadlesson(self):
            w = await Awh_AnimeLoadPkg().getData("https://animego.me/anime/podzemele-vkusnostey-2481")
            print(w)

    class Card(Awh_AnimeDvi.DviCard): pass

    class LookUp(Awh_AnimeDvi.DviLookUp): pass
