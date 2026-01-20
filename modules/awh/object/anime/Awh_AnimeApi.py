# Пользовательский файл для логики
from .Awh_AnimeDpi import Awh_AnimeDpi, Awh_AnimeObj
from ..animegenre.Awh_AnimeGenreApi import Awh_AnimeGenreApi

class Awh_AnimeApi(Awh_AnimeDpi):
    async def register(self, data):
        w = await self.findByMnemocode(data['url'])
        if w is not None:
            return w
        obj = await self.insert()
        obj.bReleased = data['released']
        obj.sCaption = data['name']
        obj.nSeries = data['series']
        obj.sUrl = data['url']
        obj.sUrlImg = data['urlImg']
        await self.update(obj)
        await Awh_AnimeGenreApi().fillGenreByAnime(obj.id, data['genre'])
        return obj.id
