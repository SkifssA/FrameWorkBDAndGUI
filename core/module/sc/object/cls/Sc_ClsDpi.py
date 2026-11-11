# Системный файл для логики
from core.sdk import EmptyLogic, EmptyObj
from dataclasses import dataclass
from typing import Optional

@dataclass
class Sc_ClsObj(EmptyObj):
    id:int
    sCode:Optional[str] = None
    sName:Optional[str] = None
    nID:Optional[int] = None

class Sc_ClsDpi(EmptyLogic[Sc_ClsObj]):
    _classObj = Sc_ClsObj
    _attrForHL = ['sName']
    _attrForMC = ['sCode']

    def _getNameClass(self):
        return "Sc_Cls"

    def calcHeadLine(self, rop:Sc_ClsObj)->str:
        return f'{rop.sName}'

    def calcMnemoCode(self, rop:Sc_ClsObj)->str:
        return f'{rop.sCode}'

    def setsCode(self, obj:Sc_ClsObj, value): obj.sCode = value; self.after_setter(obj, 'sCode')
    def setsName(self, obj:Sc_ClsObj, value): obj.sName = value; self.after_setter(obj, 'sName')
    def setnID(self, obj:Sc_ClsObj, value): obj.nID = value; self.after_setter(obj, 'nID')
