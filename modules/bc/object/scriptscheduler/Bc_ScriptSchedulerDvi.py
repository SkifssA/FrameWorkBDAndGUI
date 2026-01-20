# Системный файл для интерфейса
from core.base import BaseAvi, Selection
from .Bc_ScriptSchedulerApi import Bc_ScriptSchedulerApi, Bc_ScriptSchedulerObj

class Bc_ScriptSchedulerDvi(BaseAvi):
    thisApi = Bc_ScriptSchedulerApi
    class DviDefault(BaseAvi.DefaultDefault):
        async def onRefresh(self):
            return """
            SELECT t.id,
                   t.gid,
                   t.sNameScript,
                   t.sNameModule,
                   t.bRepeat,
                   t.nHour,
                   t.nMinute,
                   t.nSec,
                   t.bUsed
            FROM Bc_ScriptScheduler AS t
                
            """

        def onRefreshExt(self):
            return """
            with t as ( select 
                
              )
            select 
            from t
                
            """

        async def thisRop(self)->Bc_ScriptSchedulerObj:
            return await super().thisRop()

        def thisApi(self)->Bc_ScriptSchedulerApi:
            return super().thisApi()
        
        def setsNameScript(self, sender, app_data, user_data): self.thisApi().setsNameScript(self.obj, app_data); self.afterSetter()
        def setsNameModule(self, sender, app_data, user_data): self.thisApi().setsNameModule(self.obj, app_data); self.afterSetter()
        def setbRepeat(self, sender, app_data, user_data): self.thisApi().setbRepeat(self.obj, app_data); self.afterSetter()
        def setnHour(self, sender, app_data, user_data): self.thisApi().setnHour(self.obj, app_data); self.afterSetter()
        def setnMinute(self, sender, app_data, user_data): self.thisApi().setnMinute(self.obj, app_data); self.afterSetter()
        def setnSec(self, sender, app_data, user_data): self.thisApi().setnSec(self.obj, app_data); self.afterSetter()
        def setbUsed(self, sender, app_data, user_data): self.thisApi().setbUsed(self.obj, app_data); self.afterSetter()

    class DviList(DviDefault, BaseAvi.DefaultList): pass

    class DviCard(DviDefault, BaseAvi.DefaultCard): pass

    class DviLookUp(BaseAvi.DefaultLookUp):
        async def onRefresh(self):
            return """
            SELECT t.id
                  ,t.sHeadLine 
            FROM Bc_ScriptScheduler AS t
            """
