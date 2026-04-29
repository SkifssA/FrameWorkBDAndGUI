# Системный файл для логики
import asyncio
from engine.base import BaseApi, BaseObj, gid

class Awh_GenreObj(BaseObj):
    def __init__(self):
        self.id:int = None
        self.gid:gid = None
        self.sCaption:str = None

class Awh_GenreDpi(BaseApi):
    _classObj = Awh_GenreObj

    def _getNameClass(self):
        return "Awh_Genre"

    def calcHeadLine(self, rop:Awh_GenreObj)->str:
        return f'{rop.sCaption}'

    def calcMnemoCode(self, rop:Awh_GenreObj)->str:
        return f'{rop.sCaption}'

    async def insert(self)->Awh_GenreObj:
        return await super().insert()

    async def delete(self, rop:Awh_GenreObj)->None:
        
        return await super().delete(rop)
    
    async def update(self, rop:Awh_GenreObj)->None:
        return await super().update(rop)
    
    def load(self, id: int)->Awh_GenreObj:
        return super().load(id)

    def setsCaption(self, obj:Awh_GenreObj, value): obj.sCaption = value
