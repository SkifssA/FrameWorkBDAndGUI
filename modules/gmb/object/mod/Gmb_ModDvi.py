# Системный файл для интерфейса
from engine.base import BaseAvi, Selection, Event
from .Gmb_ModApi import Gmb_ModApi, Gmb_ModObj

class Gmb_ModDvi(BaseAvi):
    thisApi = Gmb_ModApi

    class DviDefault(BaseAvi.DefaultDefault):
        def onRefresh(self):
            return """
                SELECT t.id,
                    t.gid,
                    t.sCaption,
                    t.sReviewer,
                    t.sIdGitReviewer
                FROM Gmb_Mod AS t
                    
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

        def thisRop(self)->Gmb_ModObj:
            return super().thisRop()

        def thisApi(self)->Gmb_ModApi:
            return super().thisApi()
        
        def setsCaption(self, event:Event.SetterEvent): self.thisApi().setsCaption(self.thisRop(), event.value); self.afterSetter()
        def setsReviewer(self, event:Event.SetterEvent): self.thisApi().setsReviewer(self.thisRop(), event.value); self.afterSetter()
        def setsIdGitReviewer(self, event:Event.SetterEvent): self.thisApi().setsIdGitReviewer(self.thisRop(), event.value); self.afterSetter()

    class DviList(DviDefault, BaseAvi.DefaultList): pass

    class DviCard(DviDefault, BaseAvi.DefaultCard): pass

    class DviLookUp(BaseAvi.DefaultLookUp):
        def onRefresh(self):
            return """
            SELECT t.id
                ,t.sHeadLine 
            FROM Gmb_Mod AS t
            """
