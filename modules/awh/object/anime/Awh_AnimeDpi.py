# Системный файл для логики
import asyncio
from core.base import BaseApi, BaseObj, gid

class Awh_AnimeObj(BaseObj):
    def __init__(self):
        self.id:int = None
        self.gid:gid = None
        self.sCaption:str = None
        self.nSeries:int = None
        self.bReleased:int = None
        self.sUrl:str = None
        self.sUrlImg:str = None

class Awh_AnimeDpi(BaseApi):
    _classObj = Awh_AnimeObj

    def _getNameClass(self):
        return "Awh_Anime"

    def calcHeadLine(self, rop:Awh_AnimeObj)->str:
        return f'{rop.sCaption}'

    def calcMnemoCode(self, rop:Awh_AnimeObj)->str:
        return f'{rop.sUrl}'

    async def insert(self)->Awh_AnimeObj:
        return await super().insert()

    async def delete(self, rop:Awh_AnimeObj)->None:
        from ...object.animegenre.Awh_AnimeGenreApi import Awh_AnimeGenreApi
        d = await Awh_AnimeGenreApi()._getAllByAttr('idAnime', rop.id)
        if d: asyncio.gather(*(Awh_AnimeGenreApi().delete(i) for i in d))
        return await super().delete(rop)
    
    async def update(self, rop:Awh_AnimeObj)->None:
        return await super().update(rop)
    
    def load(self, id: int)->Awh_AnimeObj:
        return super().load(id)

    def setsCaption(self, obj:Awh_AnimeObj, value): obj.sCaption = value
    def setnSeries(self, obj:Awh_AnimeObj, value): obj.nSeries = value
    def setbReleased(self, obj:Awh_AnimeObj, value): obj.bReleased = value
    def setsUrl(self, obj:Awh_AnimeObj, value): obj.sUrl = value
    def setsUrlImg(self, obj:Awh_AnimeObj, value): obj.sUrlImg = value
