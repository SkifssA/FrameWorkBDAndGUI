# Системный файл для интерфейса
from engine.base import BaseAvi, Selection, Event
from .Bc_ScriptSchedulerApi import Bc_ScriptSchedulerApi, Bc_ScriptSchedulerObj

class Bc_ScriptSchedulerDvi(BaseAvi):
    thisApi = Bc_ScriptSchedulerApi

    class DviDefault(BaseAvi.DefaultDefault):
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
        
        def setsNameScript(self, event:Event.SetterEvent): self.thisApi().setsNameScript(self.thisRop(), event.value); self.afterSetter()
        def setsNameModule(self, event:Event.SetterEvent): self.thisApi().setsNameModule(self.thisRop(), event.value); self.afterSetter()
        def setbRepeat(self, event:Event.SetterEvent): self.thisApi().setbRepeat(self.thisRop(), event.value); self.afterSetter()
        def setnTime(self, event:Event.SetterEvent): self.thisApi().setnTime(self.thisRop(), event.value); self.afterSetter()
        def setidTimeLine(self, event:Event.SetterEvent): self.thisApi().setidTimeLine(self.thisRop(), event.value); self.afterSetter()
        def setidTimeLineHL(self, event:Event.SetterEvent): idLook = event.user_data.getId(event.value); self.thisApi().setidTimeLine(self.thisRop(), idLook); self.afterSetter()
        def setbUsed(self, event:Event.SetterEvent): self.thisApi().setbUsed(self.thisRop(), event.value); self.afterSetter()

    class DviList(DviDefault, BaseAvi.DefaultList): pass

    class DviCard(DviDefault, BaseAvi.DefaultCard): 
        def onRefresh(self):
            return self.thisApi().load(self.idItem)

    class DviLookUp(BaseAvi.DefaultLookUp):
        def onRefresh(self):
            return """
            SELECT t.id
                ,t.sHeadLine 
            FROM Bc_ScriptScheduler AS t
            """
