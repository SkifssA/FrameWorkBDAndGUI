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

    def getPrefixModule(self, sCode:str)->str:
        """Префикс модуля класса по его коду (имени таблицы).

        Ищем класс в реестрах META_FILE всех модулей (ядро core/module/* и
        пользовательские module/*); если класс не найден — фолбэк на соглашение
        имён 'Префикс_Имя' (core.package.ModuleManagerPkg.getModule).
        """
        from core.package.ModuleManagerPkg import ModuleManagerPkg, getModule

        mgr = ModuleManagerPkg()
        for name in mgr.getNameModule():
            try:
                metaCache = mgr._getModule(name).META_FILE
            except Exception:
                continue
            if any(f.startswith(f"{sCode}.") for f in metaCache):
                return name
        return getModule(sCode)