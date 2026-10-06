# Системный файл для логики
from core.sdk import EmptyApi, EmptyObj
from dataclasses import dataclass

@dataclass
class Awh_AnimeObj(EmptyObj):
    id:int
    sCaption:str = None
    nSeries:int = None
    bReleased:int = None
    sUrl:str = None
    sUrlImg:str = None
    sComment:str = None

class Awh_AnimeDpi(EmptyApi):
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

    def delete(self, obj:Awh_AnimeObj)->None:
        from module.awh import Awh_AnimeGenreApi
        for i in Awh_AnimeGenreApi().getAllByAttr('idAnime', obj.id) or []:
            Awh_AnimeGenreApi().delete(i)
        return super().delete(obj)
    
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
