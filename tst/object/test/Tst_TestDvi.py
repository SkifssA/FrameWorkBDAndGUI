# Системный файл для интерфейса
from core.base import BaseAvi, Selection
from .Tst_TestApi import Tst_TestApi, Tst_TestObj

class Tst_TestDvi(BaseAvi):
    thisApi = Tst_TestApi
    class DviDefault(BaseAvi.DefaultDefault):
        async def onRefresh(self):
            return """
            SELECT t.id,
                   t.gid,
                   t.sName,
                   t.nQty,
                   t.idConfig,
                   t1.sHeadLine as idConfigHL,
                   t.idConfigLook,
                   t2.sHeadLine as idConfigLookHL,
                   t.bEnd
            FROM Tst_Test AS t
                LEFT JOIN Tst_TestLookUp t1 ON t1.id = t.idConfig
                LEFT JOIN Tst_TestLookUp t2 ON t2.id = t.idConfigLook
            """

        def onRefreshExt(self):
            return """
            with t as ( select 
                :idConfig as idConfig,
                :idConfigLook as idConfigLook
              )
            select t1.sHeadLine as idConfigHL,
                   t2.sHeadLine as idConfigLookHL
            from t
                LEFT JOIN Tst_TestLookUp t1 ON t1.id = t.idConfig
                LEFT JOIN Tst_TestLookUp t2 ON t2.id = t.idConfigLook
            """

        async def thisRop(self)->Tst_TestObj:
            return await super().thisRop()

        def thisApi(self)->Tst_TestApi:
            return super().thisApi()
        
        def setsName(self, sender, app_data, user_data): self.thisApi().setsName(self.obj, app_data); self.afterSetter()
        def setnQty(self, sender, app_data, user_data): self.thisApi().setnQty(self.obj, app_data); self.afterSetter()
        def setidConfig(self, sender, app_data, user_data): self.thisApi().setidConfig(self.obj, app_data); self.afterSetter()
        def setidConfigLook(self, sender, app_data, user_data): self.thisApi().setidConfigLook(self.obj, app_data); self.afterSetter()
        def setidConfigLookHL(self, sender, app_data, user_data): idLook = user_data.getId(app_data); self.thisApi().setidConfigLook(self.obj, idLook); self.afterSetter()
        def setbEnd(self, sender, app_data, user_data): self.thisApi().setbEnd(self.obj, app_data); self.afterSetter()

    class DviList(DviDefault, BaseAvi.DefaultList): pass

    class DviCard(DviDefault, BaseAvi.DefaultCard): pass

    class DviLookUp(BaseAvi.DefaultLookUp):
        async def onRefresh(self):
            return """
            SELECT t.id
                  ,t.sHeadLine 
            FROM Tst_Test AS t
            """
