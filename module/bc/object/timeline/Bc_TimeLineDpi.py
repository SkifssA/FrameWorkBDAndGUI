# Системный файл для логики
from core.sdk import EmptyLogic, EmptyObj
from dataclasses import dataclass
from typing import Optional

@dataclass
class Bc_TimeLineObj(EmptyObj):
    id:int
    sCode:Optional[str] = None
    sName:Optional[str] = None

class Bc_TimeLineDpi(EmptyLogic[Bc_TimeLineObj]):
    _classObj = Bc_TimeLineObj
    _attrForHL = ['sName']
    _attrForMC = ['sCode']

    def _getNameClass(self):
        return "Bc_TimeLine"

    def calcHeadLine(self, rop:Bc_TimeLineObj)->str:
        return f'{rop.sName}'

    def calcMnemoCode(self, rop:Bc_TimeLineObj)->str:
        return f'{rop.sCode}'

    def setsCode(self, obj:Bc_TimeLineObj, value): obj.sCode = value; self.after_setter(obj, 'sCode')
    def setsName(self, obj:Bc_TimeLineObj, value): obj.sName = value; self.after_setter(obj, 'sName')
