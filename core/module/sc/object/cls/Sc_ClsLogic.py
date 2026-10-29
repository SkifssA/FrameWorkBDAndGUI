# Пользовательский файл для логики
from .Sc_ClsDpi import Sc_ClsDpi, Sc_ClsObj

class Sc_ClsLogic(Sc_ClsDpi):
    def register(self, sCode:str, sName:str):
        if x:=self.getByMnemocode(sCode):
            obj = x
        else:
            obj = super().insert()
            self.setsCode(obj, sCode)
            self.setnID(obj, 1)
        
        self.setsName(obj, sName)
        self.commit(obj)
        return obj

    def getID(self, sCode:str)->int:
        obj = self.getByMnemocode(sCode)
        if obj:
            id_ = obj.nID + 1
            self.setnID(obj, id_)
            self.commit(obj)
            return id_
        return 1