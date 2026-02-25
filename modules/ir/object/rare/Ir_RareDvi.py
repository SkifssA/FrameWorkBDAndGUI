# Системный файл для интерфейса
from core.base import BaseAvi, Selection, Event
from .Ir_RareApi import Ir_RareApi, Ir_RareObj

class Ir_RareDvi(BaseAvi):
    thisApi = Ir_RareApi

    class DviDefault(BaseAvi.DefaultDefault):
        async def onRefresh(self):
            return """
                SELECT t.id,
                    t.gid,
                    t.sCaption,
                    t.sCode,
                    t.sColor
                FROM Ir_Rare AS t
                    
                """

        def onRefreshExt(self):
            return """
                with t as ( select 
                    
                )
                select 
                from t
                    
                """

        def thisRop(self)->Ir_RareObj:
            return super().thisRop()

        def thisApi(self)->Ir_RareApi:
            return super().thisApi()
        
        def setsCaption(self, event:Event.SetterEvent): self.thisApi().setsCaption(self.thisRop(), event.value); self.afterSetter()
        def setsCode(self, event:Event.SetterEvent): self.thisApi().setsCode(self.thisRop(), event.value); self.afterSetter()
        def setsColor(self, event:Event.SetterEvent): self.thisApi().setsColor(self.thisRop(), event.value); self.afterSetter()

    class DviList(DviDefault, BaseAvi.DefaultList): pass

    class DviCard(DviDefault, BaseAvi.DefaultCard): pass

    class DviLookUp(BaseAvi.DefaultLookUp):
        async def onRefresh(self):
            return """
            SELECT t.id
                ,t.sHeadLine 
            FROM Ir_Rare AS t
            """
