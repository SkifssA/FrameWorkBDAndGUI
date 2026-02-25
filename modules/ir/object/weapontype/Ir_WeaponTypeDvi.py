# Системный файл для интерфейса
from core.base import BaseAvi, Selection, Event
from .Ir_WeaponTypeApi import Ir_WeaponTypeApi, Ir_WeaponTypeObj

class Ir_WeaponTypeDvi(BaseAvi):
    thisApi = Ir_WeaponTypeApi

    class DviDefault(BaseAvi.DefaultDefault):
        async def onRefresh(self):
            return """
                SELECT t.id,
                    t.gid,
                    t.sCaption,
                    t.sCode
                FROM Ir_WeaponType AS t
                    
                """

        def onRefreshExt(self):
            return """
                with t as ( select 
                    
                )
                select 
                from t
                    
                """

        def thisRop(self)->Ir_WeaponTypeObj:
            return super().thisRop()

        def thisApi(self)->Ir_WeaponTypeApi:
            return super().thisApi()
        
        def setsCaption(self, event:Event.SetterEvent): self.thisApi().setsCaption(self.thisRop(), event.value); self.afterSetter()
        def setsCode(self, event:Event.SetterEvent): self.thisApi().setsCode(self.thisRop(), event.value); self.afterSetter()

    class DviList(DviDefault, BaseAvi.DefaultList): pass

    class DviCard(DviDefault, BaseAvi.DefaultCard): pass

    class DviLookUp(BaseAvi.DefaultLookUp):
        async def onRefresh(self):
            return """
            SELECT t.id
                ,t.sHeadLine 
            FROM Ir_WeaponType AS t
            """
