# Системный файл для интерфейса
from .Awh_AnimeGenreLogic import Awh_AnimeGenreLogic, Awh_AnimeGenreObj
from core.sdk import EmptyPub


class Awh_AnimeGenreDvi(EmptyPub):
    thisLogic = Awh_AnimeGenreLogic

    class DviDefault(EmptyPub.Default):
        def structuredQuery(self):
            return """
                SELECT t.id,
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
                    :id as id,
                    :idAnime as idAnime,
            :idGenre as idGenre
                )
                select
                    t.id,
                  t1.sHeadLine as idAnimeHL,
                    t2.sHeadLine as idGenreHL
                from t
                    LEFT JOIN Awh_Anime t1 ON t1.id = t.idAnime
            LEFT JOIN Awh_Genre t2 ON t2.id = t.idGenre
                """

        def thisRop(self) -> Awh_AnimeGenreObj:
            return super().thisRop()

        def thisLogic(self) -> Awh_AnimeGenreLogic:
            return super().thisLogic()

    class DviList(DviDefault, EmptyPub.List):
        pass

    class DviCard(DviDefault):
        def onRefresh(self):
            return self.thisLogic().load(self.idItem)

    class DviLookUp:
        def onRefresh(self):
            return """
            SELECT t.id
                ,t.sHeadLine 
            FROM Awh_AnimeGenre AS t
            """
