# Системный файл для интерфейса
from core.base import BaseAvi, Selection, Event
from .Ir_ItemApi import Ir_ItemApi, Ir_ItemObj

class Ir_ItemDvi(BaseAvi):
    thisApi = Ir_ItemApi

    class DviDefault(BaseAvi.DefaultDefault):
        async def onRefresh(self):
            return """
                SELECT t.id,
                    t.gid,
                    t.gidScr
                FROM Ir_Item AS t
                    
                """

        def onRefreshExt(self):
            return """
                with t as ( select 
                    
                )
                select 
                from t
                    
                """

        def thisRop(self)->Ir_ItemObj:
            return super().thisRop()

        def thisApi(self)->Ir_ItemApi:
            return super().thisApi()
        
        def setgidScr(self, event:Event.SetterEvent): self.thisApi().setgidScr(self.thisRop(), event.value); self.afterSetter()

    class DviList(DviDefault, BaseAvi.DefaultList): pass

    class DviCard(DviDefault, BaseAvi.DefaultCard): pass

    class DviLookUp(BaseAvi.DefaultLookUp):
        async def onRefresh(self):
            return """
            SELECT t.id
                ,t.sHeadLine 
            FROM Ir_Item AS t
            """
