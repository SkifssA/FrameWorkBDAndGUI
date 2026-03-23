# Пользовательский файл для интерфейса
import dearpygui.dearpygui as dpg
from core.base.oper import SetOper
from .Awh_AnimeDvi import Awh_AnimeDvi
import webbrowser
from core.base.modal import *

from ..Awh_AnimeLoadPkg import Awh_AnimeLoadPkg

class Awh_AnimeAvi(Awh_AnimeDvi):
    class List(Awh_AnimeDvi.DviList):
        @SetOper(label='Загрузить', img='9')
        async def uploadlesson(self):
            async def registerAnime(kattr):
                a = await Awh_AnimeLoadPkg().getData(kattr['sUrl'])
                await self.thisApi().register(a)
                await self.refresh()
            
            Awh_AnimeAvi.cardSetUrlAnime().openModal(registerAnime, ['sUrl'])

        @SetOper(label='Cайт', img='8')
        async def openWeb(self):
            webbrowser.open(self.getAttr('sUrl'))

        @SetOper(label='ВК', img='8')
        async def openWebVk(self):
            temp = 'https://vkvideo.ru/?hd=1&q=аниме%20{name}%20все%20серии%20Anime%20➤%20AniPlanet'
            name = self.getAttr('sCaption').replace(' ', '%20')
            webbrowser.open(temp.format(name=name))

        def onRefresh(self):
            return f"""
            SELECT t.id,
                   t.gid,
                   t.sCaption,
                   t.nSeries,
                   t.bReleased,
                   t.sUrl,
                   GROUP_CONCAT(t2.sHeadLine, ', ') AS lGenres,
                   t.sUrlImg
            FROM Awh_Anime AS t
            LEFT JOIN Awh_AnimeGenre t1 on t1.idAnime = t.id
            LEFT JOIN Awh_Genre t2 on t2.id = t1.idGenre
            GROUP BY t.id, t.gid, t.sCaption, t.nSeries, t.bReleased, t.sUrl
            """

        def openCh(self):
            from modules.bc.object.file.Bc_FileAvi import Bc_FileAvi
            yield Bc_FileAvi.cardFileView_sUrl(locat='right')

        async def setflt_sName(self):
            await self.refresh()

    class Card(Awh_AnimeDvi.DviCard): pass

    class CardSetUrlAnime(Card):
        class addData:
            def __init__(self):
                self.sUrl:str = None

        async def getObj(self):
            return self.addData()
        
        @SetOper(label='Выбрать', order=-1, isVisible=False, img='10', isLong=True)
        async def returnResult(self):
            if self.getAttr("sUrl") is None or self.getAttr("sUrl").strip() == '':
                ErrorModal('Значение атрибута \"Ссылка на аниме\" не может быть пустым').show()
            else:
                return await super().returnResult()

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