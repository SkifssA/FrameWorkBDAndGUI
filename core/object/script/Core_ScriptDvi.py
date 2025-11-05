# Системный файл для интерфейса
from core.base import BaseAvi, Selection
from .Core_ScriptApi import Core_ScriptApi, Core_ScriptObj

class Core_ScriptDvi(BaseAvi):
    thisApi = Core_ScriptApi
    class DviList(BaseAvi.DefaultList):
        showAttr = ['sAction', 'nVersion']
        selection = lambda self: Selection(self.getTag())
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

    class DviLookUp(BaseAvi.DefaultLookUp):
        async def onRefresh(self):
            return """
            SELECT t.id
                  ,t.sHeadLine 
            FROM Core_Script AS t
            """
