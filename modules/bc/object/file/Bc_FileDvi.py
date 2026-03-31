# Системный файл для интерфейса
from core.base import BaseAvi, Selection, Event
from .Bc_FileApi import Bc_FileApi, Bc_FileObj

class Bc_FileDvi(BaseAvi):
    thisApi = Bc_FileApi

    class DviDefault(BaseAvi.DefaultDefault):
        def onRefresh(self):
            return """
                SELECT t.id,
                    t.gid,
                    t.gidScr,
                    t.sCaption,
                    t.sSuffix,
                    t.sPath
                FROM Bc_File AS t
                    
                """

        def onRefreshExt(self):
            return """
                with t as ( select 
                    
                )
                select 
                from t
                    
                """

        def thisRop(self)->Bc_FileObj:
            return super().thisRop()

        def thisApi(self)->Bc_FileApi:
            return super().thisApi()
        
        def setgidScr(self, event:Event.SetterEvent): self.thisApi().setgidScr(self.thisRop(), event.value); self.afterSetter()
        def setsCaption(self, event:Event.SetterEvent): self.thisApi().setsCaption(self.thisRop(), event.value); self.afterSetter()
        def setsSuffix(self, event:Event.SetterEvent): self.thisApi().setsSuffix(self.thisRop(), event.value); self.afterSetter()
        def setsPath(self, event:Event.SetterEvent): self.thisApi().setsPath(self.thisRop(), event.value); self.afterSetter()

    class DviList(DviDefault, BaseAvi.DefaultList): pass

    class DviCard(DviDefault, BaseAvi.DefaultCard): pass

    class DviLookUp(BaseAvi.DefaultLookUp):
        async def onRefresh(self):
            return """
            SELECT t.id
                ,t.sHeadLine 
            FROM Bc_File AS t
            """
