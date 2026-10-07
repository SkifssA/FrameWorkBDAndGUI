# Системный файл для интерфейса
from .Awh_AnimeLogic import Awh_AnimeLogic, Awh_AnimeObj
from core.sdk import EmptyPub

class Awh_AnimeDvi:
    thisLogic = Awh_AnimeLogic

    class DviDefault(EmptyPub.Default):
        def structuredQuery(self):
            return """
                SELECT t.id,
                    t.sCaption,
                    t.nSeries,
                    t.bReleased,
                    t.sUrl,
                    t.sUrlImg,
                    t.sComment
                FROM Awh_Anime AS t
                    
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

        def thisRop(self)->Awh_AnimeObj:
            return super().thisRop()

        def thisLogic(self)->Awh_AnimeLogic:
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
            FROM Awh_Anime AS t
            """
