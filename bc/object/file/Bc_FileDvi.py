# Системный файл для интерфейса
from core.base import BaseAvi, Selection
from .Bc_FileApi import Bc_FileApi, Bc_FileObj

class Bc_FileDvi(BaseAvi):
    thisApi = Bc_FileApi
    class DviDefault(BaseAvi.DefaultDefault):
        async def onRefresh(self):
            return """
            SELECT t.id,
                   t.gid,
                   t.gidScr,
                   t.sCaption,
                   t.sSuffix,
                   t.sPath
            FROM Bc_File AS t
                   
            """

        async def thisRop(self)->Bc_FileObj:
            return await super().thisRop()

        def thisApi(self)->Bc_FileApi:
            return super().thisApi()
        
        def setgidScr(self, sender, app_data, user_data): self.thisApi().setgidScr(self.obj, app_data); self.afterSetter()
        def setsCaption(self, sender, app_data, user_data): self.thisApi().setsCaption(self.obj, app_data); self.afterSetter()
        def setsSuffix(self, sender, app_data, user_data): self.thisApi().setsSuffix(self.obj, app_data); self.afterSetter()
        def setsPath(self, sender, app_data, user_data): self.thisApi().setsPath(self.obj, app_data); self.afterSetter()

    class DviList(DviDefault, BaseAvi.DefaultList): pass

    class DviCard(DviDefault, BaseAvi.DefaultCard): pass

    class DviLookUp(BaseAvi.DefaultLookUp):
        async def onRefresh(self):
            return """
            SELECT t.id
                  ,t.sHeadLine 
            FROM Bc_File AS t
            """
