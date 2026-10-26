# Системный файл для логики
from core.sdk import EmptyLogic, EmptyObj
from dataclasses import dataclass
from typing import Optional

@dataclass
class Awh_AnimeObj(EmptyObj):
    id:int
    sCaption:Optional[str] = None
    nSeries:Optional[int] = None
    bReleased:Optional[int] = None
    sUrl:Optional[str] = None
    sUrlImg:Optional[str] = None
    sComment:Optional[str] = None

class Awh_AnimeDpi(EmptyLogic[Awh_AnimeObj]):
    _classObj = Awh_AnimeObj

    def _getNameClass(self):
        return "Awh_Anime"

    def calcHeadLine(self, rop:Awh_AnimeObj)->str:
        return f'{rop.sCaption}'

    def calcMnemoCode(self, rop:Awh_AnimeObj)->str:
        return f'{rop.sUrl}'

    def setsCaption(self, obj:Awh_AnimeObj, value): obj.sCaption = value
    def setnSeries(self, obj:Awh_AnimeObj, value): obj.nSeries = value
    def setbReleased(self, obj:Awh_AnimeObj, value): obj.bReleased = value
    def setsUrl(self, obj:Awh_AnimeObj, value): obj.sUrl = value
    def setsUrlImg(self, obj:Awh_AnimeObj, value): obj.sUrlImg = value
    def setsComment(self, obj:Awh_AnimeObj, value): obj.sComment = value
