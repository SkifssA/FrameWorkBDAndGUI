# Пользовательский файл для логики
from .Core_ClassDpi import Core_ClassDpi, Core_ClassObj

class Core_ClassApi(Core_ClassDpi):
    def register(self, sCode, sCaption):
        id_ = self.findByMnemocode(sCode)
        if id_ is not None:
            obj = self.load(id_)
        else:
            obj = self.insert()
            self.setsCode(obj, sCode)
        self.setsCaption(obj, sCaption)
        self.update(obj)
        return obj
