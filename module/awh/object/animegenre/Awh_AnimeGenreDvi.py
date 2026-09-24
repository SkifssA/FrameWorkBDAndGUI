# Системный файл для интерфейса
from core.empty import EmptyAvi
from .Awh_AnimeGenreApi import Awh_AnimeGenreApi, Awh_AnimeGenreObj
from core.type.Event import SetterEvent

class Awh_AnimeGenreDvi(EmptyAvi):
    thisApi = Awh_AnimeGenreApi

    class DviDefault(EmptyAvi.Default):
        def onRefresh(self):
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

        def thisRop(self)->Awh_AnimeGenreObj:
            return super().thisRop()

        def thisApi(self)->Awh_AnimeGenreApi:
            return super().thisApi()

        def setidAnime(self, event:SetterEvent): self.thisApi().setidAnime(self.thisRop(), event.value.getValue()['value']); self.afterSetter()
        def setidAnimeHL(self, event:SetterEvent): 
            from ...object.anime.Awh_AnimeAvi import Awh_AnimeAvi
            Awh_AnimeAvi().proccessById(event, self.getAttr('idAnime'), lambda x: self.thisApi().setidAnime(self.thisRop(), x['id'])); self.afterSetter()
        def setidGenre(self, event:SetterEvent): self.thisApi().setidGenre(self.thisRop(), event.value.getValue()['value']); self.afterSetter()
        def setidGenreHL(self, event:SetterEvent): 
            from ...object.genre.Awh_GenreAvi import Awh_GenreAvi
            Awh_GenreAvi().proccessById(event, self.getAttr('idGenre'), lambda x: self.thisApi().setidGenre(self.thisRop(), x['id'])); self.afterSetter()
        
    class DviList(DviDefault, EmptyAvi.List): pass

    class DviCard(DviDefault, EmptyAvi.Card): 
        def onRefresh(self):
            return self.thisApi().load(self.idItem)

    class DviLookUp(EmptyAvi.LookUp):
        def onRefresh(self):
            return """
            SELECT t.id
                ,t.sHeadLine 
            FROM Awh_AnimeGenre AS t
            """
