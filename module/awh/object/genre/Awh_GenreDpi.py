# Системный файл для логики
from core.sdk import EmptyLogic, EmptyObj
from dataclasses import dataclass

@dataclass
class Awh_GenreObj(EmptyObj):
    id:int
    sCaption:str = None

class Awh_GenreDpi(EmptyLogic):
    _classObj = Awh_GenreObj

    def _getNameClass(self):
        return "Awh_Genre"

    def calcHeadLine(self, rop:Awh_GenreObj)->str:
        return f'{rop.sCaption}'

    def calcMnemoCode(self, rop:Awh_GenreObj)->str:
        return f'{rop.sCaption}'

    def insert(self)->Awh_GenreObj:
        return super().insert()

    def getByMnemocode(self, value)->Awh_GenreObj|None:   
        return super().getByMnemocode(value)

    def delete(self, obj:Awh_GenreObj)->None:
        
        return super().delete(obj)
    
    def update(self, rop:Awh_GenreObj)->None:
        return super().update(rop)
    
    def load(self, id: int)->Awh_GenreObj:
        return super().load(id)

    def setsCaption(self, obj:Awh_GenreObj, value): obj.sCaption = value
