# Пользовательский файл для логики
from datetime import datetime as dt

from .Bc_LogDpi import Bc_LogDpi, Bc_LogObj

class Bc_LogApi(Bc_LogDpi):
    async def insertByMess(self, sText:str):
        obj = await self.insert()
        time = dt.now()
        format_of_time = time.strftime("%H:%M")
        self.setsText(obj, f'[{format_of_time}] {sText}')
        await self.update(obj)
