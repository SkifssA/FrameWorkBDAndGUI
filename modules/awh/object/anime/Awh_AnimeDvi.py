# Системный файл для интерфейса
from engine.base import BaseAvi, Selection, Event
from .Awh_AnimeApi import Awh_AnimeApi, Awh_AnimeObj

class Awh_AnimeDvi(BaseAvi):
    thisApi = Awh_AnimeApi

    class DviDefault(BaseAvi.DefaultDefault):
        def onRefresh(self):
            return """
                SELECT t.id,
                    t.gid,
                    t.sCaption,
                    t.nSeries,
                    t.bReleased,
                    t.sUrl,
                    t.sUrlImg,
                    t.sComment
                FROM Awh_Anime AS t
                    
                """

        def onRefreshExt(self):
            return """
                with t as ( select 
                    :id as id
                    
                )
                select
                    t.id
                  
                from t
                    
                """

        def thisRop(self)->Awh_AnimeObj:
            return super().thisRop()

        def thisApi(self)->Awh_AnimeApi:
            return super().thisApi()
        
        def setsCaption(self, event:Event.SetterEvent): self.thisApi().setsCaption(self.thisRop(), event.value); self.afterSetter()
        def setnSeries(self, event:Event.SetterEvent): self.thisApi().setnSeries(self.thisRop(), event.value); self.afterSetter()
        def setbReleased(self, event:Event.SetterEvent): self.thisApi().setbReleased(self.thisRop(), event.value); self.afterSetter()
        def setsUrl(self, event:Event.SetterEvent): self.thisApi().setsUrl(self.thisRop(), event.value); self.afterSetter()
        def setsUrlImg(self, event:Event.SetterEvent): self.thisApi().setsUrlImg(self.thisRop(), event.value); self.afterSetter()
        def setsComment(self, event:Event.SetterEvent): self.thisApi().setsComment(self.thisRop(), event.value); self.afterSetter()

    class DviList(DviDefault, BaseAvi.DefaultList): pass

    class DviCard(DviDefault, BaseAvi.DefaultCard): pass

    class DviLookUp(BaseAvi.DefaultLookUp):
        def onRefresh(self):
            return """
            SELECT t.id
                ,t.sHeadLine 
            FROM Awh_Anime AS t
            """
