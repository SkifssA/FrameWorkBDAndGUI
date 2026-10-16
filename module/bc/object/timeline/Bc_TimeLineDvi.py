# Системный файл для интерфейса
from .Bc_TimeLineLogic import Bc_TimeLineLogic, Bc_TimeLineObj
from core.sdk import EmptyPub

class Bc_TimeLineDvi(EmptyPub):
    thisLogic = Bc_TimeLineLogic

    class DviDefault(EmptyPub.Default):
        def structuredQuery(self):
            return """
                SELECT t.id,
                    t.sCode,
                    t.sName
                FROM Bc_TimeLine AS t
                    
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

        def thisRop(self)->Bc_TimeLineObj:
            return super().thisRop()

        def thisLogic(self)->Bc_TimeLineLogic:
            return super().thisLogic()

        
        
    class DviList(DviDefault, EmptyPub.List): pass

    class DviCard(DviDefault, EmptyPub.Card):...

    class DviLookUp:
        def onRefresh(self):
            return """
            SELECT t.id
                ,t.sHeadLine 
            FROM Bc_TimeLine AS t
            """
