# Системный файл для интерфейса
from core.base import BaseAvi, Selection, Event
from .Bc_IconsApi import Bc_IconsApi, Bc_IconsObj

class Bc_IconsDvi(BaseAvi):
    thisApi = Bc_IconsApi

    class DviDefault(BaseAvi.DefaultDefault):
        def onRefresh(self):
            return """
                SELECT t.id,
                    t.gid,
                    t.sCode,
                    t.sPath
                FROM Bc_Icons AS t
                    
                """

        def onRefreshExt(self):
            return """
                with t as ( select 
                    
                )
                select 
                from t
                    
                """

        def thisRop(self)->Bc_IconsObj:
            return super().thisRop()

        def thisApi(self)->Bc_IconsApi:
            return super().thisApi()
        
        def setsCode(self, event:Event.SetterEvent): self.thisApi().setsCode(self.thisRop(), event.value); self.afterSetter()
        def setsPath(self, event:Event.SetterEvent): self.thisApi().setsPath(self.thisRop(), event.value); self.afterSetter()

    class DviList(DviDefault, BaseAvi.DefaultList): pass

    class DviCard(DviDefault, BaseAvi.DefaultCard): pass

    class DviLookUp(BaseAvi.DefaultLookUp):
        def onRefresh(self):
            return """
            SELECT t.id
                ,t.sHeadLine 
            FROM Bc_Icons AS t
            """
