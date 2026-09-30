# Системный файл для интерфейса
from core.sdk import EmptyAvi, SetterEvent
from .Bc_ScriptSchedulerApi import Bc_ScriptSchedulerApi, Bc_ScriptSchedulerObj

class Bc_ScriptSchedulerDvi(EmptyAvi):
    thisApi = Bc_ScriptSchedulerApi

    class DviDefault(EmptyAvi.Default):
        def onRefresh(self):
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
                    :id as id,
                    :idTimeLine as idTimeLine
                )
                select
                    t.id,
                  t1.sHeadLine as idTimeLineHL
                from t
                    LEFT JOIN Bc_TimeLine t1 ON t1.id = t.idTimeLine
                """

        def thisRop(self)->Bc_ScriptSchedulerObj:
            return super().thisRop()

        def thisApi(self)->Bc_ScriptSchedulerApi:
            return super().thisApi()

        def setsNameScript(self, event:SetterEvent): self.thisApi().setsNameScript(self.thisRop(), event.value); self.afterSetter('sNameScript')
        def setsNameModule(self, event:SetterEvent): self.thisApi().setsNameModule(self.thisRop(), event.value); self.afterSetter('sNameModule')
        def setbRepeat(self, event:SetterEvent): self.thisApi().setbRepeat(self.thisRop(), event.value); self.afterSetter('bRepeat')
        def setnTime(self, event:SetterEvent): self.thisApi().setnTime(self.thisRop(), event.value); self.afterSetter('nTime')
        def setidTimeLine(self, event:SetterEvent): self.thisApi().setidTimeLine(self.thisRop(), event.value); self.afterSetter('idTimeLine')
        def setidTimeLineHL(self, event:SetterEvent): self.thisApi().setidTimeLine(self.thisRop(), event.value); self.afterSetter('idTimeLineHL')
        def setbUsed(self, event:SetterEvent): self.thisApi().setbUsed(self.thisRop(), event.value); self.afterSetter('bUsed')
        
    class DviList(DviDefault, EmptyAvi.List): pass

    class DviCard(DviDefault, EmptyAvi.Card): 
        def onRefresh(self):
            return self.thisApi().load(self.idItem)

    class DviLookUp(EmptyAvi.LookUp):
        def onRefresh(self):
            return """
            SELECT t.id
                ,t.sHeadLine 
            FROM Bc_ScriptScheduler AS t
            """
