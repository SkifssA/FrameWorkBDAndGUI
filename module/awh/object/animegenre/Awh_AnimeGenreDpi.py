# Системный файл для логики
from core.sdk import EmptyApi, EmptyObj
from dataclasses import dataclass

@dataclass
class Awh_AnimeGenreObj(EmptyObj):
    id:int
    idAnime:int = None
    idGenre:int = None

class Awh_AnimeGenreDpi(EmptyApi):
    _classObj = Awh_AnimeGenreObj

    def _getNameClass(self):
        return "Awh_AnimeGenre"

    def calcHeadLine(self, rop:Awh_AnimeGenreObj)->str:
        return f'{rop.id}'

    def calcMnemoCode(self, rop:Awh_AnimeGenreObj)->str:
        return f'{rop.id}'

    def insert(self)->Awh_AnimeGenreObj:
        return super().insert()

    def getByMnemocode(self, value)->Awh_AnimeGenreObj|None:   
        return super().getByMnemocode(value)

    def delete(self, obj:Awh_AnimeGenreObj)->None:
        
        return super().delete(obj)
    
    def update(self, rop:Awh_AnimeGenreObj)->None:
        return super().update(rop)
    
    def load(self, id: int)->Awh_AnimeGenreObj:
        return super().load(id)

    def setidAnime(self, obj:Awh_AnimeGenreObj, value): obj.idAnime = value
    def setidGenre(self, obj:Awh_AnimeGenreObj, value): obj.idGenre = value
