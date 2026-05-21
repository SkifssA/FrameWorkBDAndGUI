# Пользовательский файл для логики
from .Awh_AnimeDpi import Awh_AnimeDpi, Awh_AnimeObj
from ..animegenre.Awh_AnimeGenreApi import Awh_AnimeGenreApi

class Awh_AnimeApi(Awh_AnimeDpi):
    def register(self, data):
        obj = self.findByMnemocode(data['url'])
        if obj is None:
            obj = self.insert()
            obj.sUrl = data['url']
            Awh_AnimeGenreApi().fillGenreByAnime(obj.id, data['genre'])
        else:
            obj = self.load(obj)

        obj.bReleased = data['released']
        obj.sCaption = data['name']
        obj.nSeries = data['series']
        obj.sUrlImg = data['urlImg']
        obj.sComment = data['comment']
        self.update(obj)
        return obj.id
    
    async def updateAnime(self):
        from ..Awh_AnimeLoadPkg import Awh_AnimeLoadPkg
        lv = await self.getAll()
        for i in lv:
            obj = self.load(i['id'])
            a = await Awh_AnimeLoadPkg().getData(obj.sUrl)
            self.register(a)
