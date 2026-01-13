# Пользовательский файл для интерфейса
from core.base.BaseOper import SetOper
from .Awh_AnimeDvi import Awh_AnimeDvi
import webbrowser
from core.base.BaseAvi import BaseAvi

from ..Awh_AnimeLoadPkg import Awh_AnimeLoadPkg

class Awh_AnimeAvi(Awh_AnimeDvi):
    class List(Awh_AnimeDvi.DviList):
        @SetOper(label='Тест загрузки данных')
        async def uploadlesson(self):
            async def w(**kattr):
                a = await Awh_AnimeLoadPkg().getData(kattr['sUrl'])
                await self.thisApi().register(a)
                await self.refresh()
            
            await Awh_AnimeAvi.cardSetUrlAnime().openModal(w, ['sUrl'])


        @SetOper(label='Тест открытия веб')
        async def openWeb(self):
            webbrowser.open(self.getAttr('sUrl'))

    class Card(Awh_AnimeDvi.DviCard): pass

    class CardSetUrlAnime(Card):
        class addData:
            def __init__(self):
                self.sUrl:str = None

        async def getObj(self):
            return self.addData()

    class LookUp(Awh_AnimeDvi.DviLookUp): pass

    @classmethod
    def list(cls, **kwargs)->List:
        return cls.typeMeta(cls.List, **kwargs)
    
    @classmethod
    def card(cls, **kwargs)->Card:
        return cls.typeMeta(cls.Card, **kwargs)
    
    @classmethod
    def cardSetUrlAnime(cls, **kwargs)->CardSetUrlAnime:
        return cls.typeMeta(cls.CardSetUrlAnime, **kwargs)