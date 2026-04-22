# Системный файл для интерфейса
from core.base import BaseAvi, Selection, Event
from .Awh_AnimeGenreApi import Awh_AnimeGenreApi, Awh_AnimeGenreObj

class Awh_AnimeGenreDvi(BaseAvi):
    thisApi = Awh_AnimeGenreApi

    class DviDefault(BaseAvi.DefaultDefault):
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
                    :id as id
                    :idAnime as idAnime,
            :idGenre as idGenre
                )
                select
                    t.id
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
        
        def setidAnime(self, event:Event.SetterEvent): self.thisApi().setidAnime(self.thisRop(), event.value); self.afterSetter()
        def setidAnimeHL(self, event:Event.SetterEvent): event.user_data._getAvi()().proccessById(event, self.getAttr('idAnime'), lambda x: self.thisApi().setidAnime(self.thisRop(), x['id'])); self.afterSetter()
        def setidGenre(self, event:Event.SetterEvent): self.thisApi().setidGenre(self.thisRop(), event.value); self.afterSetter()
        def setidGenreHL(self, event:Event.SetterEvent): event.user_data._getAvi()().proccessById(event, self.getAttr('idGenre'), lambda x: self.thisApi().setidGenre(self.thisRop(), x['id'])); self.afterSetter()

    class DviList(DviDefault, BaseAvi.DefaultList): pass

    class DviCard(DviDefault, BaseAvi.DefaultCard): pass

    class DviLookUp(BaseAvi.DefaultLookUp):
        def onRefresh(self):
            return """
            SELECT t.id
                ,t.sHeadLine 
            FROM Awh_AnimeGenre AS t
            """
