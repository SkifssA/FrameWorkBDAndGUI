# Пользовательский файл для логики
import asyncio
from concurrent.futures import Future

from .Bc_TimeLineDpi import Bc_TimeLineDpi, Bc_TimeLineObj

class Bc_TimeLineApi(Bc_TimeLineDpi):

    sHour = "Hour"
    sMinute = "Minute"
    sSecond = "Second"

    idHour = (lambda: Bc_TimeLineDpi().findByMnemocode("Hour"))()
    idMinute = (lambda: Bc_TimeLineDpi().findByMnemocode("Minute"))()
    idSecond = (lambda: Bc_TimeLineDpi().findByMnemocode("Second"))()
                                              
    def register(self, sCode:str, sName:str):
        obj = self.findByMnemocode(sCode)
        if obj is None:
            obj = self.insert()
            self.setsCode(obj, sCode)
        self.setsName(obj, sName)
        self.update(obj)

    async def dataInstall(self):
        self.register(Bc_TimeLineApi.sHour, "Час")
        self.register(Bc_TimeLineApi.sMinute, "Минута")
        self.register(Bc_TimeLineApi.sSecond, "Секунда")
