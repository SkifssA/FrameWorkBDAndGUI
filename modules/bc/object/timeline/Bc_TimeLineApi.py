# Пользовательский файл для логики
from engine.package.LazyVal import LazyVal 
from .Bc_TimeLineDpi import Bc_TimeLineDpi, Bc_TimeLineObj

class Bc_TimeLineApi(Bc_TimeLineDpi):

    sHour = "Hour"
    sMinute = "Minute"
    sSecond = "Second"

    idHour = LazyVal(lambda: Bc_TimeLineDpi().findByMnemocode("Hour"))
    idMinute = LazyVal(lambda: Bc_TimeLineDpi().findByMnemocode("Minute"))
    idSecond = LazyVal(lambda: Bc_TimeLineDpi().findByMnemocode("Second"))
                                              
    def register(self, sCode:str, sName:str):
        obj = self.getByMnemocode(sCode)
        if obj is None:
            obj = self.insert()
            self.setsCode(obj, sCode)
        self.setsName(obj, sName)
        self.update(obj)

    async def dataInstall(self):
        self.register(Bc_TimeLineApi.sHour, "Час")
        self.register(Bc_TimeLineApi.sMinute, "Минута")
        self.register(Bc_TimeLineApi.sSecond, "Секунда")
