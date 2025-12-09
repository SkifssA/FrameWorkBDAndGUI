# Системный файл для интерфейса
from core.base import BaseAvi, Selection
from .Core_AttrApi import Core_AttrApi, Core_AttrObj

class Core_AttrDvi(BaseAvi):
    thisApi = Core_AttrApi
    class DviDefault(BaseAvi.DefaultDefault):
        async def onRefresh(self):
            return """
            SELECT t.id,
                   t.gid,
                   t.idTab,
                   t1.sHeadLine as idTabHL,
                   t.sCode,
                   t.sCaption,
                   t.sType,
                   t.sRefClass
            FROM Core_Attr AS t
                   LEFT JOIN Core_Class t1 ON t1.id = t.idTab
            """

        async def thisRop(self)->Core_AttrObj:
            return await super().thisRop()

        def thisApi(self)->Core_AttrApi:
            return super().thisApi()
        
        def setidTab(self, sender, app_data, user_data): self.thisApi().setidTab(self.obj, app_data)
        def setsCode(self, sender, app_data, user_data): self.thisApi().setsCode(self.obj, app_data)
        def setsCaption(self, sender, app_data, user_data): self.thisApi().setsCaption(self.obj, app_data)
        def setsType(self, sender, app_data, user_data): self.thisApi().setsType(self.obj, app_data)
        def setsRefClass(self, sender, app_data, user_data): self.thisApi().setsRefClass(self.obj, app_data)

    class DviList(DviDefault, BaseAvi.DefaultList): pass

    class DviCard(DviDefault, BaseAvi.DefaultCard): pass

    class DviLookUp(BaseAvi.DefaultLookUp):
        async def onRefresh(self):
            return """
            SELECT t.id
                  ,t.sHeadLine 
            FROM Core_Attr AS t
            """
