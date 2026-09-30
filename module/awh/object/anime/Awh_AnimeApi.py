# Пользовательский файл для логики
from .Awh_AnimeDpi import Awh_AnimeDpi, Awh_AnimeObj
from ..animegenre.Awh_AnimeGenreApi import Awh_AnimeGenreApi
from core.sdk import asyncRun

class Awh_AnimeApi(Awh_AnimeDpi):
    def register(self, data: dict):
        obj = self.getByMnemocode(data['url'])
        if obj is None:
            obj = self.insert()
            self.setsUrl(obj, data['url'])
            Awh_AnimeGenreApi().fillGenreByAnime(obj.id, data['genre'])

        self.setbReleased(obj, data['released'])
        self.setsCaption(obj, data['name'])
        self.setnSeries(obj, data['series'])
        self.setsUrlImg(obj, data['urlImg'])
        self.setsComment(obj, data['comment'])
        self.update(obj)
        return obj.id

    def addByUrl(self, sUrl):
        from ..Awh_AnimeLoadPkg import Awh_AnimeLoadPkg
        obj = asyncRun(Awh_AnimeLoadPkg().init())
        data = asyncRun(obj.getData(sUrl))
        self.register(data)

    def updateAnime(self):
        from ..Awh_AnimeLoadPkg import Awh_AnimeLoadPkg
        lv = self.getAllByAttr('bReleased', 0)
        animeLoad = asyncRun(Awh_AnimeLoadPkg().init())
        for i in lv:
            a = asyncRun(animeLoad.getData(i.sUrl))
            self.register(a)