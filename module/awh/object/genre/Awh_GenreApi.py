# Пользовательский файл для логики
from .Awh_GenreDpi import Awh_GenreDpi, Awh_GenreObj

class Awh_GenreApi(Awh_GenreDpi):
    def register(self, name):
        w = self.getByMnemocode(name)
        if w is not None:
            return w.id
        obj = self.insert()
        self.setsCaption(obj, name)
        self.update(obj)
        return obj.id
