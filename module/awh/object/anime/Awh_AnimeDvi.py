# Системный файл для интерфейса
from .Awh_AnimeApi import Awh_AnimeApi, Awh_AnimeObj
from core.sdk import EmptyAvi

class Awh_AnimeDvi:
    thisApi = Awh_AnimeApi

    class DviDefault(EmptyAvi.Default):
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

        def thisApi(self)->Awh_AnimeApi:
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
            FROM Awh_Anime AS t
            """
