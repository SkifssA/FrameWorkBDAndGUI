# Системный файл для интерфейса
from .Awh_GenreApi import Awh_GenreApi, Awh_GenreObj
from core.sdk import EmptyAvi

class Awh_GenreDvi:
    thisApi = Awh_GenreApi

    class DviDefault(EmptyAvi.Default):
        def structuredQuery(self):
            return """
                SELECT t.id,
                    t.sCaption
                FROM Awh_Genre AS t
                    
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

        def thisRop(self)->Awh_GenreObj:
            return super().thisRop()

        def thisApi(self)->Awh_GenreApi:
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
            FROM Awh_Genre AS t
            """
