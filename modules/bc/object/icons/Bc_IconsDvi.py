# Системный файл для интерфейса
from core.base import BaseAvi, Selection
from .Bc_IconsApi import Bc_IconsApi, Bc_IconsObj

class Bc_IconsDvi(BaseAvi):
    thisApi = Bc_IconsApi
    class DviDefault(BaseAvi.DefaultDefault):
        async def onRefresh(self):
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

        async def thisRop(self)->Bc_IconsObj:
            return await super().thisRop()

        def thisApi(self)->Bc_IconsApi:
            return super().thisApi()
        
        def setsCode(self, sender, app_data, user_data): self.thisApi().setsCode(self.obj, app_data); self.afterSetter()
        def setsPath(self, sender, app_data, user_data): self.thisApi().setsPath(self.obj, app_data); self.afterSetter()

    class DviList(DviDefault, BaseAvi.DefaultList): pass

    class DviCard(DviDefault, BaseAvi.DefaultCard): pass

    class DviLookUp(BaseAvi.DefaultLookUp):
        async def onRefresh(self):
            return """
            SELECT t.id
                ,t.sHeadLine 
            FROM Bc_Icons AS t
            """
