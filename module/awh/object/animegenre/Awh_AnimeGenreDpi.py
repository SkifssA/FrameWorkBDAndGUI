# Системный файл для логики
from core.sdk import EmptyLogic, EmptyObj
from dataclasses import dataclass
from typing import Optional

@dataclass
class Awh_AnimeGenreObj(EmptyObj):
    id:int
    idAnime:Optional[int] = None
    idGenre:Optional[int] = None

class Awh_AnimeGenreDpi(EmptyLogic[Awh_AnimeGenreObj]):
    _classObj = Awh_AnimeGenreObj

    def _getNameClass(self):
        return "Awh_AnimeGenre"

    def calcHeadLine(self, rop:Awh_AnimeGenreObj)->str:
        return f'{rop.id}'

    def calcMnemoCode(self, rop:Awh_AnimeGenreObj)->str:
        return f'{rop.id}'

    def setidAnime(self, obj:Awh_AnimeGenreObj, value): obj.idAnime = value
    def setidGenre(self, obj:Awh_AnimeGenreObj, value): obj.idGenre = value
