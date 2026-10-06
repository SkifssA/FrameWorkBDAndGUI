# Системный файл для интерфейса
from engineQT.sdk import EmptyAvi, SetterEvent
from .Bc_ScriptSchedulerApi import Bc_ScriptSchedulerApi, Bc_ScriptSchedulerObj

class Bc_ScriptSchedulerDvi(EmptyAvi):
    thisApi = Bc_ScriptSchedulerApi

    class DviDefault(EmptyAvi.Default):
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

        def thisRop(self)->Bc_ScriptSchedulerObj:
            return super().thisRop()

        def thisApi(self)->Bc_ScriptSchedulerApi:
            return super().thisApi()

        
        
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
