# Системный файл для интерфейса
from .Bc_ScriptSchedulerLogic import Bc_ScriptSchedulerLogic, Bc_ScriptSchedulerObj
from core.sdk import EmptyPub

class Bc_ScriptSchedulerDvi:
    thisApi = Bc_ScriptSchedulerLogic

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

        def thisRop(self)->Bc_ScriptSchedulerObj:
            return super().thisRop()

        def thisLogic(self)->Bc_ScriptSchedulerLogic:
            return super().thisLogic()

        
        
    class DviList(DviDefault, EmptyPub.List): pass

    class DviCard(DviDefault): 
        def onRefresh(self):
            return self.thisLogic().load(self.idItem)

    class DviLookUp:
        def onRefresh(self):
            return """
            SELECT t.id
                ,t.sHeadLine 
            FROM Bc_ScriptScheduler AS t
            """
