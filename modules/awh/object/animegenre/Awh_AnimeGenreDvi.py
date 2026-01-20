# Системный файл для интерфейса
from core.base import BaseAvi, Selection
from .Awh_AnimeGenreApi import Awh_AnimeGenreApi, Awh_AnimeGenreObj

class Awh_AnimeGenreDvi(BaseAvi):
    thisApi = Awh_AnimeGenreApi
    class DviDefault(BaseAvi.DefaultDefault):
        async def onRefresh(self):
            return """
            SELECT t.id,
                   t.gid,
                   t.idAnime,
                   t1.sHeadLine as idAnimeHL,
                   t.idGenre,
                   t2.sHeadLine as idGenreHL
            FROM Awh_AnimeGenre AS t
                LEFT JOIN Awh_Anime t1 ON t1.id = t.idAnime
                LEFT JOIN Awh_Genre t2 ON t2.id = t.idGenre
            """

        def onRefreshExt(self):
            return """
            with t as ( select 
                :idAnime as idAnime,
                :idGenre as idGenre
              )
            select t1.sHeadLine as idAnimeHL,
                   t2.sHeadLine as idGenreHL
            from t
                LEFT JOIN Awh_Anime t1 ON t1.id = t.idAnime
                LEFT JOIN Awh_Genre t2 ON t2.id = t.idGenre
            """

        async def thisRop(self)->Awh_AnimeGenreObj:
            return await super().thisRop()

        def thisApi(self)->Awh_AnimeGenreApi:
            return super().thisApi()
        
        def setidAnime(self, sender, app_data, user_data): self.thisApi().setidAnime(self.obj, app_data); self.afterSetter()
        def setidGenre(self, sender, app_data, user_data): self.thisApi().setidGenre(self.obj, app_data); self.afterSetter()

    class DviList(DviDefault, BaseAvi.DefaultList): pass

    class DviCard(DviDefault, BaseAvi.DefaultCard): pass

    class DviLookUp(BaseAvi.DefaultLookUp):
        async def onRefresh(self):
            return """
            SELECT t.id
                  ,t.sHeadLine 
            FROM Awh_AnimeGenre AS t
            """
