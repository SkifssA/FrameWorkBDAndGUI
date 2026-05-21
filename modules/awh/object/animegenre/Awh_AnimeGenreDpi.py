# Системный файл для логики
import asyncio
from engine.base import BaseApi, BaseObj, gid

class Awh_AnimeGenreObj(BaseObj):
    def __init__(self):
        self.id:int = None
        self.gid:gid = None
        self.idAnime:int = None
        self.idGenre:int = None

class Awh_AnimeGenreDpi(BaseApi):
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

    def delete(self, rop:Awh_AnimeGenreObj)->None:
        
        return super().delete(rop)
    
    def update(self, rop:Awh_AnimeGenreObj)->None:
        return super().update(rop)
    
    def load(self, id: int)->Awh_AnimeGenreObj:
        return super().load(id)

    def setidAnime(self, obj:Awh_AnimeGenreObj, value): obj.idAnime = value
    def setidGenre(self, obj:Awh_AnimeGenreObj, value): obj.idGenre = value
