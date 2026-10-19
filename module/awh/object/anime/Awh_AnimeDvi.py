# Системный файл для интерфейса
from .Awh_AnimeLogic import Awh_AnimeLogic, Awh_AnimeObj
from core.sdk import EmptyPub, SetterEvent, Setter

class Awh_AnimeDvi(EmptyPub):
    thisLogic = Awh_AnimeLogic

    class DviDefault(EmptyPub.Default):
        def structuredQuery(self):
            return """
                SELECT t.id,
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

        def thisLogic(self)->Awh_AnimeLogic:
            return super().thisLogic()

        @Setter
        def setsCaption(self, event:SetterEvent): self.thisLogic().setsCaption(self.thisObj(), event.value); self.afterSetter('sCaption')
        @Setter
        def setnSeries(self, event:SetterEvent): self.thisLogic().setnSeries(self.thisObj(), event.value); self.afterSetter('nSeries')
        @Setter
        def setbReleased(self, event:SetterEvent): self.thisLogic().setbReleased(self.thisObj(), event.value); self.afterSetter('bReleased')
        @Setter
        def setsUrl(self, event:SetterEvent): self.thisLogic().setsUrl(self.thisObj(), event.value); self.afterSetter('sUrl')
        @Setter
        def setsUrlImg(self, event:SetterEvent): self.thisLogic().setsUrlImg(self.thisObj(), event.value); self.afterSetter('sUrlImg')
        @Setter
        def setsComment(self, event:SetterEvent): self.thisLogic().setsComment(self.thisObj(), event.value); self.afterSetter('sComment')
        
    class DviList(DviDefault, EmptyPub.List):...

    class DviCard(DviDefault, EmptyPub.Card):...

    class DviLookUp:
        def onRefresh(self):
            return """
            SELECT t.id
                ,t.sHeadLine 
            FROM Awh_Anime AS t
            """
