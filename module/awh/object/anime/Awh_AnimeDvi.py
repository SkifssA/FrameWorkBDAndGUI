# Системный файл для интерфейса
from core.empty import EmptyAvi
from .Awh_AnimeApi import Awh_AnimeApi, Awh_AnimeObj
from core.type.Event import SetterEvent

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

        def setsCaption(self, event:SetterEvent): self.thisApi().setsCaption(self.thisRop(), event.value.getValue()['value']); self.afterSetter()
        def setnSeries(self, event:SetterEvent): self.thisApi().setnSeries(self.thisRop(), event.value.getValue()['value']); self.afterSetter()
        def setbReleased(self, event:SetterEvent): self.thisApi().setbReleased(self.thisRop(), event.value.getValue()['value']); self.afterSetter()
        def setsUrl(self, event:SetterEvent): self.thisApi().setsUrl(self.thisRop(), event.value.getValue()['value']); self.afterSetter()
        def setsUrlImg(self, event:SetterEvent): self.thisApi().setsUrlImg(self.thisRop(), event.value.getValue()['value']); self.afterSetter()
        def setsComment(self, event:SetterEvent): self.thisApi().setsComment(self.thisRop(), event.value.getValue()['value']); self.afterSetter()
        
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
