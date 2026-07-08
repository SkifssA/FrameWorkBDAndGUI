# Системный файл для интерфейса
from engine.base import BaseAvi, Selection, Event
from .Gmb_ModApi import Gmb_ModApi, Gmb_ModObj

class Gmb_ModDvi(BaseAvi):
    thisApi = Gmb_ModApi

    class DviDefault(BaseAvi.DefaultDefault):
        def onRefresh(self):
            return """
                SELECT t.id,
                    t.gid,
                    t.idTask,
                    t1.sHeadLine as idTaskHL,
                    t.sCapTask
                FROM Gmb_Mod AS t
                    LEFT JOIN Gmb_Task t1 ON t1.id = t.idTask
                """

        def onRefreshExt(self):
            return """
                with t as ( select 
                    :id as id
                    :idTask as idTask
                )
                select
                    t.id
                  t1.sHeadLine as idTaskHL
                from t
                    LEFT JOIN Gmb_Task t1 ON t1.id = t.idTask
                """

        def thisRop(self)->Gmb_ModObj:
            return super().thisRop()

        def thisApi(self)->Gmb_ModApi:
            return super().thisApi()
        
        def setidTask(self, event:Event.SetterEvent): self.thisApi().setidTask(self.thisRop(), event.value); self.afterSetter()
        def setidTaskHL(self, event:Event.SetterEvent): event.user_data._getAvi()().proccessById(event, self.getAttr('idTask'), lambda x: self.thisApi().setidTask(self.thisRop(), x['id'])); self.afterSetter()
        def setsCapTask(self, event:Event.SetterEvent): self.thisApi().setsCapTask(self.thisRop(), event.value); self.afterSetter()

    class DviList(DviDefault, BaseAvi.DefaultList): pass

    class DviCard(DviDefault, BaseAvi.DefaultCard): pass

    class DviLookUp(BaseAvi.DefaultLookUp):
        def onRefresh(self):
            return """
            SELECT t.id
                ,t.sHeadLine 
            FROM Gmb_Mod AS t
            """
