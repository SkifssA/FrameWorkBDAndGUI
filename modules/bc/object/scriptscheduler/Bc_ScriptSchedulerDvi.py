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
                    t.nTime,
                    t.idTimeLine,
                    t1.sHeadLine as idTimeLineHL,
                    t.bUsed
                FROM Bc_ScriptScheduler AS t
                    LEFT JOIN Bc_TimeLine t1 ON t1.id = t.idTimeLine
                """

        def onRefreshExt(self):
            return """
                with t as ( select 
                    :idTimeLine as idTimeLine
                )
                select t1.sHeadLine as idTimeLineHL
                from t
                    LEFT JOIN Bc_TimeLine t1 ON t1.id = t.idTimeLine
                """

        async def thisRop(self)->Bc_ScriptSchedulerObj:
            return await super().thisRop()

        def thisApi(self)->Bc_ScriptSchedulerApi:
            return super().thisApi()
        
        def setsNameScript(self, sender, app_data, user_data): self.thisApi().setsNameScript(self.obj, app_data); self.afterSetter()
        def setsNameModule(self, sender, app_data, user_data): self.thisApi().setsNameModule(self.obj, app_data); self.afterSetter()
        def setbRepeat(self, sender, app_data, user_data): self.thisApi().setbRepeat(self.obj, app_data); self.afterSetter()
        def setnTime(self, sender, app_data, user_data): self.thisApi().setnTime(self.obj, app_data); self.afterSetter()
        def setidTimeLine(self, sender, app_data, user_data): self.thisApi().setidTimeLine(self.obj, app_data); self.afterSetter()
        def setidTimeLineHL(self, sender, app_data, user_data): idLook = user_data.getId(app_data); self.thisApi().setidTimeLine(self.obj, idLook); self.afterSetter()
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
