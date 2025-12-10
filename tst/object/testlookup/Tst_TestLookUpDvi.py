# Системный файл для интерфейса
from core.base import BaseAvi, Selection
from .Tst_TestLookUpApi import Tst_TestLookUpApi, Tst_TestLookUpObj

class Tst_TestLookUpDvi(BaseAvi):
    thisApi = Tst_TestLookUpApi
    class DviDefault(BaseAvi.DefaultDefault):
        async def onRefresh(self):
            return """
            SELECT t.id,
                   t.gid,
                   t.sName
            FROM Tst_TestLookUp AS t
                   
            """

        async def thisRop(self)->Tst_TestLookUpObj:
            return await super().thisRop()

        def thisApi(self)->Tst_TestLookUpApi:
            return super().thisApi()
        
        def setsName(self, sender, app_data, user_data): self.thisApi().setsName(self.obj, app_data); self.afterSetter()

    class DviList(DviDefault, BaseAvi.DefaultList): pass

    class DviCard(DviDefault, BaseAvi.DefaultCard): pass

    class DviLookUp(BaseAvi.DefaultLookUp):
        async def onRefresh(self):
            return """
            SELECT t.id
                  ,t.sHeadLine 
            FROM Tst_TestLookUp AS t
            """
