# Системный файл для интерфейса
from core.base import BaseAvi, Selection
from .Awh_GenreApi import Awh_GenreApi, Awh_GenreObj

class Awh_GenreDvi(BaseAvi):
    thisApi = Awh_GenreApi
    class DviDefault(BaseAvi.DefaultDefault):
        async def onRefresh(self):
            return """
            SELECT t.id,
                   t.gid,
                   t.sCaption
            FROM Awh_Genre AS t
                
            """

        def onRefreshExt(self):
            return """
            with t as ( select 
                
              )
            select 
            from t
                
            """

        async def thisRop(self)->Awh_GenreObj:
            return await super().thisRop()

        def thisApi(self)->Awh_GenreApi:
            return super().thisApi()
        
        def setsCaption(self, sender, app_data, user_data): self.thisApi().setsCaption(self.obj, app_data); self.afterSetter()

    class DviList(DviDefault, BaseAvi.DefaultList): pass

    class DviCard(DviDefault, BaseAvi.DefaultCard): pass

    class DviLookUp(BaseAvi.DefaultLookUp):
        async def onRefresh(self):
            return """
            SELECT t.id
                  ,t.sHeadLine 
            FROM Awh_Genre AS t
            """
