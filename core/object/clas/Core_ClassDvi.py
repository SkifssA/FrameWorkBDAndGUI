# Системный файл для интерфейса
from core.base import BaseAvi, Selection
from .Core_ClassApi import Core_ClassApi, Core_ClassObj

class Core_ClassDvi(BaseAvi):
    thisApi = Core_ClassApi
    class DviDefault(BaseAvi.DefaultDefault):
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

        def thisApi(self)->Core_ClassApi:
            return super().thisApi()

    class DviList(DviDefault, BaseAvi.DefaultList): pass

    class DviCard(DviDefault, BaseAvi.DefaultCard): pass

    class DviLookUp(BaseAvi.DefaultLookUp):
        async def onRefresh(self):
            return """
            SELECT t.id
                  ,t.sHeadLine 
            FROM Core_Class AS t
            """
