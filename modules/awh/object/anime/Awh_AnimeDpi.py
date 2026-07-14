# Системный файл для логики
import asyncio
from engine.base import BaseApi, BaseObj, gid

class Awh_AnimeObj(BaseObj):
    def __init__(self):
        self.id:int = None
        self.gid:gid = None
        self.sCaption:str = None
        self.nSeries:int = None
        self.bReleased:int = None
        self.sUrl:str = None
        self.sUrlImg:str = None
        self.sComment:str = None

class Awh_AnimeDpi(BaseApi):
    _classObj = Awh_AnimeObj

    def _getNameClass(self):
        return "Awh_Anime"

    def calcHeadLine(self, rop:Awh_AnimeObj)->str:
        return f'{rop.sCaption}'

    def calcMnemoCode(self, rop:Awh_AnimeObj)->str:
        return f'{rop.sUrl}'

    def insert(self)->Awh_AnimeObj:
        return super().insert()

    def getByMnemocode(self, value)->Awh_AnimeObj|None:   
        return super().getByMnemocode(value)

    def delete(self, rop:Awh_AnimeObj)->None:
        from ...object.animegenre.Awh_AnimeGenreApi import Awh_AnimeGenreApi
        for i in Awh_AnimeGenreApi()._getAllByAttr('idAnime', rop.id) or []:
            Awh_AnimeGenreApi().delete(i)
        return super().delete(rop)
    
    def update(self, rop:Awh_AnimeObj)->None:
        return super().update(rop)
    
    def load(self, id: int)->Awh_AnimeObj:
        return super().load(id)

    def setsCaption(self, obj:Awh_AnimeObj, value): obj.sCaption = value
    def setnSeries(self, obj:Awh_AnimeObj, value): obj.nSeries = value
    def setbReleased(self, obj:Awh_AnimeObj, value): obj.bReleased = value
    def setsUrl(self, obj:Awh_AnimeObj, value): obj.sUrl = value
    def setsUrlImg(self, obj:Awh_AnimeObj, value): obj.sUrlImg = value
    def setsComment(self, obj:Awh_AnimeObj, value): obj.sComment = value
