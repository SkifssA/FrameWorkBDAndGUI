# Системный файл для интерфейса
from core.base import BaseAvi, Selection
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

        async def thisRop(self)->Bc_ConfigObj:
            return await super().thisRop()

        def thisApi(self)->Bc_ConfigApi:
            return super().thisApi()

    class DviList(DviDefault, BaseAvi.DefaultList): pass

    class DviCard(DviDefault, BaseAvi.DefaultCard): pass

    class DviLookUp(BaseAvi.DefaultLookUp):
        async def onRefresh(self):
            return """
            SELECT t.id
                  ,t.sHeadLine 
            FROM Bc_Config AS t
            """
