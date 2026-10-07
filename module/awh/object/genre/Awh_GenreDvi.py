# Системный файл для интерфейса
from .Awh_GenreLogic import Awh_GenreLogic, Awh_GenreObj
from core.sdk import EmptyPub

class Awh_GenreDvi:
    thisLogic = Awh_GenreLogic

    class DviDefault(EmptyPub.Default):
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

        def thisLogic(self)->Awh_GenreLogic:
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
            FROM Awh_Genre AS t
            """
