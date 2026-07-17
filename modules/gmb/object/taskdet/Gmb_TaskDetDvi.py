# Системный файл для интерфейса
from engine.base import BaseAvi, Selection, Event
from .Gmb_TaskDetApi import Gmb_TaskDetApi, Gmb_TaskDetObj

class Gmb_TaskDetDvi(BaseAvi):
    thisApi = Gmb_TaskDetApi

    class DviDefault(BaseAvi.DefaultDefault):
        def onRefresh(self):
            return """
                SELECT t.id,
                    t.gid,
                    t.idTask,
                    t1.sHeadLine as idTaskHL,
                    t.idMod,
                    t2.sHeadLine as idModHL,
                    t.sUlrMR,
                    t.sLastComment
                FROM Gmb_TaskDet AS t
                    LEFT JOIN Gmb_Task t1 ON t1.id = t.idTask
                    LEFT JOIN Gmb_Mod t2 ON t2.id = t.idMod
                """

        def onRefreshExt(self):
            return """
                with t as ( select 
                    :id as id,
                    :idTask as idTask,
            :idMod as idMod
                )
                select
                    t.id,
                  t1.sHeadLine as idTaskHL,
                    t2.sHeadLine as idModHL
                from t
                    LEFT JOIN Gmb_Task t1 ON t1.id = t.idTask
            LEFT JOIN Gmb_Mod t2 ON t2.id = t.idMod
                """

        def thisRop(self)->Gmb_TaskDetObj:
            return super().thisRop()

        def thisApi(self)->Gmb_TaskDetApi:
            return super().thisApi()
        
        def setidTask(self, event:Event.SetterEvent): self.thisApi().setidTask(self.thisRop(), event.value); self.afterSetter()
        def setidTaskHL(self, event:Event.SetterEvent): 
            from ...object.task.Gmb_TaskAvi import Gmb_TaskAvi
            Gmb_TaskAvi().proccessById(event, self.getAttr('idTask'), lambda x: self.thisApi().setidTask(self.thisRop(), x['id'])); self.afterSetter()
        def setidMod(self, event:Event.SetterEvent): self.thisApi().setidMod(self.thisRop(), event.value); self.afterSetter()
        def setidModHL(self, event:Event.SetterEvent): 
            from ...object.mod.Gmb_ModAvi import Gmb_ModAvi
            Gmb_ModAvi().proccessById(event, self.getAttr('idMod'), lambda x: self.thisApi().setidMod(self.thisRop(), x['id'])); self.afterSetter()
        def setsUlrMR(self, event:Event.SetterEvent): self.thisApi().setsUlrMR(self.thisRop(), event.value); self.afterSetter()
        def setsLastComment(self, event:Event.SetterEvent): self.thisApi().setsLastComment(self.thisRop(), event.value); self.afterSetter()

    class DviList(DviDefault, BaseAvi.DefaultList): pass

    class DviCard(DviDefault, BaseAvi.DefaultCard): 
        def onRefresh(self):
            return self.thisApi().load(self.idItem)

    class DviLookUp(BaseAvi.DefaultLookUp):
        def onRefresh(self):
            return """
            SELECT t.id
                ,t.sHeadLine 
            FROM Gmb_TaskDet AS t
            """
