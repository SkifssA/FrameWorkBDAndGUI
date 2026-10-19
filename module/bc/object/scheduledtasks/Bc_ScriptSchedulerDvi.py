# Системный файл для интерфейса
from .Bc_ScriptSchedulerLogic import Bc_ScriptSchedulerLogic, Bc_ScriptSchedulerObj
from core.sdk import EmptyPub, SetterEvent, Setter

class Bc_ScriptSchedulerDvi(EmptyPub):
    thisLogic = Bc_ScriptSchedulerLogic

    class DviDefault(EmptyPub.Default):
        def structuredQuery(self):
            return """
                SELECT t.id,
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

        def thisLogic(self)->Bc_ScriptSchedulerLogic:
            return super().thisLogic()

        @Setter
        def setsNameScript(self, event:SetterEvent): self.thisLogic().setsNameScript(self.thisObj(), event.value); self.afterSetter('sNameScript')
        @Setter
        def setsNameModule(self, event:SetterEvent): self.thisLogic().setsNameModule(self.thisObj(), event.value); self.afterSetter('sNameModule')
        @Setter
        def setbRepeat(self, event:SetterEvent): self.thisLogic().setbRepeat(self.thisObj(), event.value); self.afterSetter('bRepeat')
        @Setter
        def setnTime(self, event:SetterEvent): self.thisLogic().setnTime(self.thisObj(), event.value); self.afterSetter('nTime')
        @Setter
        def setidTimeLine(self, event:SetterEvent): self.thisLogic().setidTimeLine(self.thisObj(), event.value); self.afterSetter('idTimeLine')
        @Setter
        def setidTimeLineHL(self, event:SetterEvent): self.thisLogic().setidTimeLineHL(self.thisObj(), event.value); self.afterSetter('idTimeLineHL')
        @Setter
        def setbUsed(self, event:SetterEvent): self.thisLogic().setbUsed(self.thisObj(), event.value); self.afterSetter('bUsed')
        
    class DviList(DviDefault, EmptyPub.List):...

    class DviCard(DviDefault, EmptyPub.Card):...

    class DviLookUp:
        def onRefresh(self):
            return """
            SELECT t.id
                ,t.sHeadLine 
            FROM Bc_ScriptScheduler AS t
            """
