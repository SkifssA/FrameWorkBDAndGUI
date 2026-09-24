# Системный файл для логики
from core.empty import EmptyApi, EmptyObj

class Awh_GenreObj(EmptyObj):
    def __init__(self):
        self.id:int = None
        self.sCaption:str = None

class Awh_GenreDpi(EmptyApi):
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

    def delete(self, rop:Awh_GenreObj)->None:
        
        return super().delete(rop)
    
    def update(self, rop:Awh_GenreObj)->None:
        return super().update(rop)
    
    def load(self, id: int)->Awh_GenreObj:
        return super().load(id)

    def setsCaption(self, obj:Awh_GenreObj, value): obj.sCaption = value
