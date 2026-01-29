# Пользовательский файл для логики
from .Awh_AnimeDpi import Awh_AnimeDpi, Awh_AnimeObj
from ..animegenre.Awh_AnimeGenreApi import Awh_AnimeGenreApi

class Awh_AnimeApi(Awh_AnimeDpi):
    async def register(self, data):
        obj = await self.findByMnemocode(data['url'])
        if obj is None:
            obj = await self.insert()
            obj.sUrl = data['url']
            await Awh_AnimeGenreApi().fillGenreByAnime(obj.id, data['genre'])
        else:
            obj = await self.load(obj)

        obj.bReleased = data['released']
        obj.sCaption = data['name']
        obj.nSeries = data['series']
        obj.sUrlImg = data['urlImg']
        await self.update(obj)
        return obj.id
    
    async def updateAnime(self):
        from ..Awh_AnimeLoadPkg import Awh_AnimeLoadPkg
        lv = await self._findAllByAttr('bReleased', 0)
        for i in lv:
            obj = await self.load(i)
            a = await Awh_AnimeLoadPkg().getData(obj.sUrl)
            await self.register(a)
