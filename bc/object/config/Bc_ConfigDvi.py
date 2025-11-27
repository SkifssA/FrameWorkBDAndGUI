# Системный файл для интерфейса
from core.base import BaseAvi, Selection
from .Bc_ConfigApi import Bc_ConfigApi, Bc_ConfigObj

class Bc_ConfigDvi(BaseAvi):
    thisApi = Bc_ConfigApi
    class DviDefault(BaseAvi.DefaultDefault):
        selection = lambda self: Selection(self.getTag())
        async def onRefresh(self):
            return """
            SELECT t.id,
                   t.gid,
                   t.sModule,
                   t.sCaprionSetting,
                   t.sValue
            FROM Bs_Config AS t
                   
            """

        async def thisRop(self)->Bc_ConfigObj:
            return await super().thisRop()

        def thisApi(self)->Bc_ConfigApi:
            return super().thisApi()

    class DviList(DviDefault, BaseAvi.DefaultList): pass

    class DviLookUp(BaseAvi.DefaultLookUp):
        async def onRefresh(self):
            return """
            SELECT t.id
                  ,t.sHeadLine 
            FROM Bs_Config AS t
            """
