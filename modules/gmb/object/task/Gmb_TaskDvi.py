# Системный файл для интерфейса
from engine.base import BaseAvi, Selection, Event
from .Gmb_TaskApi import Gmb_TaskApi, Gmb_TaskObj

class Gmb_TaskDvi(BaseAvi):
    thisApi = Gmb_TaskApi

    class DviDefault(BaseAvi.DefaultDefault):
        def onRefresh(self):
            return """
                SELECT t.id,
                    t.gid,
                    t.nNumTask,
                    t.sCapTask,
                    t.sBranch
                FROM Gmb_Task AS t
                    
                """

        def onRefreshExt(self):
            return """
                with t as ( select 
                    :id as id
                    
                )
                select
                    t.id
                  
                from t
                    
                """

        def thisRop(self)->Gmb_TaskObj:
            return super().thisRop()

        def thisApi(self)->Gmb_TaskApi:
            return super().thisApi()
        
        def setnNumTask(self, event:Event.SetterEvent): self.thisApi().setnNumTask(self.thisRop(), event.value); self.afterSetter()
        def setsCapTask(self, event:Event.SetterEvent): 
            self.thisApi().setsCapTask(self.thisRop(), event.value); self.afterSetter()
        def setsBranch(self, event:Event.SetterEvent): self.thisApi().setsBranch(self.thisRop(), event.value); self.afterSetter()

    class DviList(DviDefault, BaseAvi.DefaultList): pass

    class DviCard(DviDefault, BaseAvi.DefaultCard): pass

    class DviLookUp(BaseAvi.DefaultLookUp):
        def onRefresh(self):
            return """
            SELECT t.id
                ,t.sHeadLine 
            FROM Gmb_Task AS t
            """
