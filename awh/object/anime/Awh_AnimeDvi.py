# Системный файл для интерфейса
from core.base import BaseAvi, Selection
from .Awh_AnimeApi import Awh_AnimeApi, Awh_AnimeObj

class Awh_AnimeDvi(BaseAvi):
    thisApi = Awh_AnimeApi
    class DviDefault(BaseAvi.DefaultDefault):
        async def onRefresh(self):
            return """
            SELECT t.id,
                   t.gid,
                   t.sCaption,
                   t.nSeries
            FROM Awh_Anime AS t
                
            """

        def onRefreshExt(self):
            return """
            with t as ( select 
                
              )
            select 
            from t
                
            """

        async def thisRop(self)->Awh_AnimeObj:
            return await super().thisRop()

        def thisApi(self)->Awh_AnimeApi:
            return super().thisApi()
        
        def setsCaption(self, sender, app_data, user_data): self.thisApi().setsCaption(self.obj, app_data); self.afterSetter()
        def setnSeries(self, sender, app_data, user_data): self.thisApi().setnSeries(self.obj, app_data); self.afterSetter()

    class DviList(DviDefault, BaseAvi.DefaultList): pass

    class DviCard(DviDefault, BaseAvi.DefaultCard): pass

    class DviLookUp(BaseAvi.DefaultLookUp):
        async def onRefresh(self):
            return """
            SELECT t.id
                  ,t.sHeadLine 
            FROM Awh_Anime AS t
            """
