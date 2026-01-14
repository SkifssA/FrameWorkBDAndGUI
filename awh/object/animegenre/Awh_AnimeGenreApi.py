# Пользовательский файл для логики
from .Awh_AnimeGenreDpi import Awh_AnimeGenreDpi, Awh_AnimeGenreObj
from ..genre.Awh_GenreApi import Awh_GenreApi

class Awh_AnimeGenreApi(Awh_AnimeGenreDpi):
    async def insertByAnimeAndGenre(self, idAnime, idGenre):
        obj = await self.insert()
        obj.idAnime = idAnime
        obj.idGenre = idGenre
        await self.update(obj)

    async def fillGenreByAnime(self, idAnime, lsNameGenre: list):
        for i in lsNameGenre:
            idGenre = await Awh_GenreApi().register(i)
            await self.insertByAnimeAndGenre(idAnime, idGenre)
