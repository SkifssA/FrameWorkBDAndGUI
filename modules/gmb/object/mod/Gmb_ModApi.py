# Пользовательский файл для логики
from .Gmb_ModDpi import Gmb_ModDpi, Gmb_ModObj

class Gmb_ModApi(Gmb_ModDpi):

    async def dataInstall(self):
        self.register("rcr", "Копылов")
        self.register("bhr", "Копылов")
        self.register("rvs", "Филин")
        self.register("tsw", "Мизинцев")
        self.register("bs", "Мизинцев")
        self.register("hrm", "Мизинцев")
        self.register("prl", "Мизинцев")
        self.register("eqp", "Мизинцев")

    def register(self, sCaption, sReviewer):
        obj = self.getByMnemocode(sCaption)
        if obj is None:
            obj = self.insert()
            self.setsReviewer(obj, sReviewer)
            self.setsCaption(obj, sCaption)
        self.update(obj)
