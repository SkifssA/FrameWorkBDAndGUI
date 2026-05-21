# Пользовательский файл для логики
from .Awh_GenreDpi import Awh_GenreDpi, Awh_GenreObj

class Awh_GenreApi(Awh_GenreDpi):
    def register(self, name):
        w = self.findByMnemocode(name)
        if w is not None:
            return w
        obj = self.insert()
        obj.sCaption = name
        self.update(obj)
        return obj.id
