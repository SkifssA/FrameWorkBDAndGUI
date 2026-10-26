# Системный файл для логики
from core.sdk import EmptyLogic, EmptyObj
from dataclasses import dataclass
from typing import Optional

@dataclass
class Awh_GenreObj(EmptyObj):
    id:int
    sCaption:Optional[str] = None

class Awh_GenreDpi(EmptyLogic[Awh_GenreObj]):
    _classObj = Awh_GenreObj

    def _getNameClass(self):
        return "Awh_Genre"

    def calcHeadLine(self, rop:Awh_GenreObj)->str:
        return f'{rop.sCaption}'

    def calcMnemoCode(self, rop:Awh_GenreObj)->str:
        return f'{rop.sCaption}'

    def setsCaption(self, obj:Awh_GenreObj, value): obj.sCaption = value
