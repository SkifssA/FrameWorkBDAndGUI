# Системный файл для логики
from core.sdk import EmptyLogic, EmptyObj
from dataclasses import dataclass
from typing import Optional

@dataclass
class Sc_ScriptsObj(EmptyObj):
    id:int
    sCode:Optional[str] = None
    idCls:Optional[int] = None
    nVer:Optional[int] = None

class Sc_ScriptsDpi(EmptyLogic[Sc_ScriptsObj]):
    _classObj = Sc_ScriptsObj
    _attrForHL = ['']
    _attrForMC = ['sCode']

    def _getNameClass(self):
        return "Sc_Scripts"

    def calcHeadLine(self, rop:Sc_ScriptsObj)->str:
        return f'{rop.id}'

    def calcMnemoCode(self, rop:Sc_ScriptsObj)->str:
        return f'{rop.sCode}'

    def setsCode(self, obj:Sc_ScriptsObj, value): obj.sCode = value; self.after_setter(obj, 'sCode')
    def setidCls(self, obj:Sc_ScriptsObj, value): obj.idCls = value; self.after_setter(obj, 'idCls')
    def setnVer(self, obj:Sc_ScriptsObj, value): obj.nVer = value; self.after_setter(obj, 'nVer')
