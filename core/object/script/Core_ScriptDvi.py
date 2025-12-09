# Системный файл для интерфейса
from core.base import BaseAvi, Selection
from .Core_ScriptApi import Core_ScriptApi, Core_ScriptObj

class Core_ScriptDvi(BaseAvi):
    thisApi = Core_ScriptApi
    class DviDefault(BaseAvi.DefaultDefault):
        async def onRefresh(self):
            return """
            SELECT t.id,
                   t.gid,
                   t.sAction,
                   t.nVersion
            FROM Core_Script AS t
                   
            """

        async def thisRop(self)->Core_ScriptObj:
            return await super().thisRop()

        def thisApi(self)->Core_ScriptApi:
            return super().thisApi()
        
        def setsAction(self, sender, app_data, user_data): self.thisApi().setsAction(self.obj, app_data)
        def setnVersion(self, sender, app_data, user_data): self.thisApi().setnVersion(self.obj, app_data)

    class DviList(DviDefault, BaseAvi.DefaultList): pass

    class DviCard(DviDefault, BaseAvi.DefaultCard): pass

    class DviLookUp(BaseAvi.DefaultLookUp):
        async def onRefresh(self):
            return """
            SELECT t.id
                  ,t.sHeadLine 
            FROM Core_Script AS t
            """
