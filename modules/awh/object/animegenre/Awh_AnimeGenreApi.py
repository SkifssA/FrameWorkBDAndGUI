# Пользовательский файл для логики
from .Awh_AnimeGenreDpi import Awh_AnimeGenreDpi, Awh_AnimeGenreObj
from ..genre.Awh_GenreApi import Awh_GenreApi

class Awh_AnimeGenreApi(Awh_AnimeGenreDpi):
    def insertByAnimeAndGenre(self, idAnime, idGenre):
        obj = self.insert()
        obj.idAnime = idAnime
        obj.idGenre = idGenre
        self.update(obj)

    def fillGenreByAnime(self, idAnime, lsNameGenre: list):
        for i in lsNameGenre:
            idGenre = Awh_GenreApi().register(i)
            self.insertByAnimeAndGenre(idAnime, idGenre)
