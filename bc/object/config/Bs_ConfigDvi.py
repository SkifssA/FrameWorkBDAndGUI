# Системный файл для интерфейса
from core.base import BaseAvi, Selection
from .Bs_ConfigApi import Bs_ConfigApi, Bs_ConfigObj

class Bs_ConfigDvi(BaseAvi):
    thisApi = Bs_ConfigApi
    class DviList(BaseAvi.DefaultList):
        showAttr = ['sModule', 'sCaprionSetting', 'sValue']
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

        async def thisRop(self)->Bs_ConfigObj:
            return await super().thisRop()

        def thisApi(self)->Bs_ConfigApi:
            return super().thisApi()

    class DviLookUp(BaseAvi.DefaultLookUp):
        async def onRefresh(self):
            return """
            SELECT t.id
                  ,t.sHeadLine 
            FROM Bs_Config AS t
            """
