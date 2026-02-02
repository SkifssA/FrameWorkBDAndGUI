# Системный файл для интерфейса
from core.base import BaseAvi, Selection
from .Bc_TimeLineApi import Bc_TimeLineApi, Bc_TimeLineObj

class Bc_TimeLineDvi(BaseAvi):
    thisApi = Bc_TimeLineApi
    class DviDefault(BaseAvi.DefaultDefault):
        async def onRefresh(self):
            return """
                SELECT t.id,
                    t.gid,
                    t.sCode,
                    t.sName
                FROM Bc_TimeLine AS t
                    
                """

        def onRefreshExt(self):
            return """
                with t as ( select 
                    
                )
                select 
                from t
                    
                """

        async def thisRop(self)->Bc_TimeLineObj:
            return await super().thisRop()

        def thisApi(self)->Bc_TimeLineApi:
            return super().thisApi()
        
        def setsCode(self, sender, app_data, user_data): self.thisApi().setsCode(self.obj, app_data); self.afterSetter()
        def setsName(self, sender, app_data, user_data): self.thisApi().setsName(self.obj, app_data); self.afterSetter()

    class DviList(DviDefault, BaseAvi.DefaultList): pass

    class DviCard(DviDefault, BaseAvi.DefaultCard): pass

    class DviLookUp(BaseAvi.DefaultLookUp):
        async def onRefresh(self):
            return """
            SELECT t.id
                ,t.sHeadLine 
            FROM Bc_TimeLine AS t
            """
