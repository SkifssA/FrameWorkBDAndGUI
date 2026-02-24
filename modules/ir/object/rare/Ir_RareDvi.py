# Системный файл для интерфейса
from core.base import BaseAvi, Selection
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

        async def thisRop(self)->Ir_RareObj:
            return await super().thisRop()

        def thisApi(self)->Ir_RareApi:
            return super().thisApi()
        
        def setsCaption(self, sender, app_data, user_data): self.thisApi().setsCaption(self.obj, app_data); self.afterSetter()
        def setsCode(self, sender, app_data, user_data): self.thisApi().setsCode(self.obj, app_data); self.afterSetter()
        def setsColor(self, sender, app_data, user_data): self.thisApi().setsColor(self.obj, app_data); self.afterSetter()

    class DviList(DviDefault, BaseAvi.DefaultList): pass

    class DviCard(DviDefault, BaseAvi.DefaultCard): pass

    class DviLookUp(BaseAvi.DefaultLookUp):
        async def onRefresh(self):
            return """
            SELECT t.id
                ,t.sHeadLine 
            FROM Ir_Rare AS t
            """
