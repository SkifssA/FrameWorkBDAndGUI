# Пользовательский файл для интерфейса
from .Awh_AnimeDvi import Awh_AnimeDvi
from core.sdk import FormConstruct, Image, Text, SetOper
import webbrowser

class Awh_AnimeAvi(Awh_AnimeDvi):
    class List(Awh_AnimeDvi.DviList): 

        @SetOper(label='Загрузить')
        def uploadAnime(self):
            data = Awh_AnimeAvi.cardSetUrlAnime().result(
                returnAttr=['sUrlLoad']
                ).openModal()

            if data.isAccept():
                sUrl = data.getResult()['sUrlLoad']
                self.thisApi().addByUrl(sUrl)
                self.refreshForm()

        @SetOper(label='Cайт')
        def openWeb(self):
            webbrowser.open(self.getSelfAttr("sUrl"))

        @SetOper(label='ВК')
        def openWebVk(self):
            temp = 'https://vkvideo.ru/?hd=1&q=аниме%20{name}%20все%20серии%20подряд%20{qty}'
            name = self.getAttr('sCaption').replace(' ', '%20')
            qty = f'1-{self.getAttr('nSeries')}'
            webbrowser.open(temp.format(name=name, qty=qty))

        def onRefresh(self):
            return f"""
            SELECT t.id,
                   t.gid,
                   t.sCaption,
                   t.nSeries,
                   t.bReleased,
                   t.sUrl,
                   GROUP_CONCAT(t2.sHeadLine, ', ') AS lGenres,
                   t.sUrlImg,
                   t.sComment
            FROM Awh_Anime AS t
            LEFT JOIN Awh_AnimeGenre t1 on t1.idAnime = t.id
            LEFT JOIN Awh_Genre t2 on t2.id = t1.idGenre
            GROUP BY t.id, t.gid, t.sCaption, t.nSeries, t.bReleased, t.sUrl
            """

        def getChilders(self):
            yield Awh_AnimeAvi.cardImgByAnime()
            yield Awh_AnimeAvi.textByAnime()

        def checwork(self):
            super().checwork()
            self.oper.isVisible(['openWebVk', ], self.getSelfAttr('bReleased'))

    class Card(Awh_AnimeDvi.DviCard):...

    class CardImgByAnime(Awh_AnimeDvi.Default, Image): 
        def onRefresh(self):
            return self.getAttr("sUrlImg")

    class TextByAnime(Awh_AnimeDvi.Default, Text):
        def onRefresh(self):
            return self.getAttr("sComment")

    class CardSetUrlAnime(Card):
            class addData:
                def __init__(self):
                    self.sUrlLoad:str = None
                     
            def onRefresh(self):
                return self.addData()
            
            def onRefreshExt(self):
                return ''
                
            def setsUrlLoad(self, event): self.obj.sUrlLoad = event.value

    @classmethod
    def list(cls): return FormConstruct(cls.List)
    @classmethod
    def card(cls): return FormConstruct(cls.Card)
    @classmethod
    def cardImgByAnime(cls): return FormConstruct(cls.CardImgByAnime)
    @classmethod
    def textByAnime(cls): return FormConstruct(cls.TextByAnime)
    @classmethod
    def cardSetUrlAnime(cls): return FormConstruct(cls.CardSetUrlAnime)