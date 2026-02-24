# Системный файл для интерфейса
from core.base import BaseAvi, Selection
from .Ir_DefTypeApi import Ir_DefTypeApi, Ir_DefTypeObj

class Ir_DefTypeDvi(BaseAvi):
    thisApi = Ir_DefTypeApi
    class DviDefault(BaseAvi.DefaultDefault):
        async def onRefresh(self):
            return """
                SELECT t.id,
                    t.gid,
                    t.sCaption,
                    t.sCode
                FROM Ir_DefType AS t
                    
                """

        def onRefreshExt(self):
            return """
                with t as ( select 
                    
                )
                select 
                from t
                    
                """

        async def thisRop(self)->Ir_DefTypeObj:
            return await super().thisRop()

        def thisApi(self)->Ir_DefTypeApi:
            return super().thisApi()
        
        def setsCaption(self, sender, app_data, user_data): self.thisApi().setsCaption(self.obj, app_data); self.afterSetter()
        def setsCode(self, sender, app_data, user_data): self.thisApi().setsCode(self.obj, app_data); self.afterSetter()

    class DviList(DviDefault, BaseAvi.DefaultList): pass

    class DviCard(DviDefault, BaseAvi.DefaultCard): pass

    class DviLookUp(BaseAvi.DefaultLookUp):
        async def onRefresh(self):
            return """
            SELECT t.id
                ,t.sHeadLine 
            FROM Ir_DefType AS t
            """
