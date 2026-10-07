# Системный файл для интерфейса
from .Bc_TimeLineApi import Bc_TimeLineApi, Bc_TimeLineObj
from core.sdk import EmptyAvi

class Bc_TimeLineDvi:
    thisApi = Bc_TimeLineApi

    class DviDefault(EmptyAvi.Default):
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

        def thisApi(self)->Bc_TimeLineApi:
            return super().thisApi()

        
        
    class DviList(DviDefault, EmptyAvi.List): pass

    class DviCard(DviDefault): 
        def onRefresh(self):
            return self.thisApi().load(self.idItem)

    class DviLookUp:
        def onRefresh(self):
            return """
            SELECT t.id
                ,t.sHeadLine 
            FROM Bc_TimeLine AS t
            """
