# Пользовательский файл для логики
import asyncio
from concurrent.futures import Future

from .Bc_TimeLineDpi import Bc_TimeLineDpi, Bc_TimeLineObj

class Bc_TimeLineApi(Bc_TimeLineDpi):

    sHour = "Hour"
    sMinute = "Minute"
    sSecond = "Second"

    idHour = None
    idMinute = None
    idSecond = None
        
    async def fill(self):
        Bc_TimeLineApi.idHour = await self.findByMnemocode(Bc_TimeLineApi.sHour)
        Bc_TimeLineApi.idMinute = await self.findByMnemocode(Bc_TimeLineApi.sMinute)
        Bc_TimeLineApi.idSecond = await self.findByMnemocode(Bc_TimeLineApi.sSecond)
                                              
    async def register(self, sCode:str, sName:str):
        obj = await self.findByMnemocode(sCode)
        if obj is None:
            obj = await self.insert()
            self.setsCode(obj, sCode)
        self.setsName(obj, sName)
        await self.update(obj)

    async def dataInstall(self):
        await self.register(Bc_TimeLineApi.sHour, "Час")
        await self.register(Bc_TimeLineApi.sMinute, "Минута")
        await self.register(Bc_TimeLineApi.sSecond, "Секунда")
