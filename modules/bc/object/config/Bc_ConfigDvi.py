# Системный файл для интерфейса
from core.base import BaseAvi, Selection, Event
from .Bc_ConfigApi import Bc_ConfigApi, Bc_ConfigObj

class Bc_ConfigDvi(BaseAvi):
    thisApi = Bc_ConfigApi

    class DviDefault(BaseAvi.DefaultDefault):
        async def onRefresh(self):
            return """
                SELECT t.id,
                    t.gid,
                    t.sModule,
                    t.sCaprionSetting,
                    t.sValue
                FROM Bc_Config AS t
                    
                """

        def onRefreshExt(self):
            return """
                with t as ( select 
                    
                )
                select 
                from t
                    
                """

        def thisRop(self)->Bc_ConfigObj:
            return super().thisRop()

        def thisApi(self)->Bc_ConfigApi:
            return super().thisApi()
        
        def setsModule(self, event:Event.SetterEvent): self.thisApi().setsModule(self.thisRop(), event.value); self.afterSetter()
        def setsCaprionSetting(self, event:Event.SetterEvent): self.thisApi().setsCaprionSetting(self.thisRop(), event.value); self.afterSetter()
        def setsValue(self, event:Event.SetterEvent): self.thisApi().setsValue(self.thisRop(), event.value); self.afterSetter()

    class DviList(DviDefault, BaseAvi.DefaultList): pass

    class DviCard(DviDefault, BaseAvi.DefaultCard): pass

    class DviLookUp(BaseAvi.DefaultLookUp):
        async def onRefresh(self):
            return """
            SELECT t.id
                ,t.sHeadLine 
            FROM Bc_Config AS t
            """
