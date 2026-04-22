# Системный файл для интерфейса
from core.base import BaseAvi, Selection, Event
from .Bc_LogApi import Bc_LogApi, Bc_LogObj

class Bc_LogDvi(BaseAvi):
    thisApi = Bc_LogApi

    class DviDefault(BaseAvi.DefaultDefault):
        def onRefresh(self):
            return """
                SELECT t.id,
                    t.gid,
                    t.sText
                FROM Bc_Log AS t
                    
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

        def thisRop(self)->Bc_LogObj:
            return super().thisRop()

        def thisApi(self)->Bc_LogApi:
            return super().thisApi()
        
        def setsText(self, event:Event.SetterEvent): self.thisApi().setsText(self.thisRop(), event.value); self.afterSetter()

    class DviList(DviDefault, BaseAvi.DefaultList): pass

    class DviCard(DviDefault, BaseAvi.DefaultCard): pass

    class DviLookUp(BaseAvi.DefaultLookUp):
        def onRefresh(self):
            return """
            SELECT t.id
                ,t.sHeadLine 
            FROM Bc_Log AS t
            """
