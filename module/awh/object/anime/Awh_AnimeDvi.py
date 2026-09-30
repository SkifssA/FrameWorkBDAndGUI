# Системный файл для интерфейса
from core.sdk import EmptyAvi, SetterEvent
from .Awh_AnimeApi import Awh_AnimeApi, Awh_AnimeObj

class Awh_AnimeDvi(EmptyAvi):
    thisApi = Awh_AnimeApi

    class DviDefault(EmptyAvi.Default):
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

        def setsCaption(self, event:SetterEvent): self.thisApi().setsCaption(self.thisRop(), event.value); self.afterSetter('sCaption')
        def setnSeries(self, event:SetterEvent): self.thisApi().setnSeries(self.thisRop(), event.value); self.afterSetter('nSeries')
        def setbReleased(self, event:SetterEvent): self.thisApi().setbReleased(self.thisRop(), event.value); self.afterSetter('bReleased')
        def setsUrl(self, event:SetterEvent): self.thisApi().setsUrl(self.thisRop(), event.value); self.afterSetter('sUrl')
        def setsUrlImg(self, event:SetterEvent): self.thisApi().setsUrlImg(self.thisRop(), event.value); self.afterSetter('sUrlImg')
        def setsComment(self, event:SetterEvent): self.thisApi().setsComment(self.thisRop(), event.value); self.afterSetter('sComment')
        
    class DviList(DviDefault, EmptyAvi.List): pass

    class DviCard(DviDefault, EmptyAvi.Card): 
        def onRefresh(self):
            return self.thisApi().load(self.idItem)

    class DviLookUp(EmptyAvi.LookUp):
        def onRefresh(self):
            return """
            SELECT t.id
                ,t.sHeadLine 
            FROM Awh_Anime AS t
            """
