# Системный файл для интерфейса
from core.base import BaseAvi
from .Core_ClassApi import Core_ClassApi, Core_ClassObj

class Core_ClassDvi(BaseAvi):
    thisApi = Core_ClassApi
    class DviList(BaseAvi.DefaultList):
        showAttr = ['sCode', 'sCaption']
        async def onRefresh(self):
            return """
            SELECT t.id,
                   t.gid,
                   t.sCode,
                   t.sCaption
            FROM Core_Class AS t
                   
            """

        async def thisRop(self)->Core_ClassObj:
            return await super().thisRop()

        async def thisApi(self)->Core_ClassApi:
            return super().thisApi()

    class DviLookUp(BaseAvi.DefaultLookUp):
        async def onRefresh(self):
            return """
            SELECT t.id
                  ,t.sHeadLine 
            FROM Core_Class AS t
            """
