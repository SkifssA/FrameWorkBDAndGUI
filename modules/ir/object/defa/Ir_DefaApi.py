# Пользовательский файл для логики
import random

from .Ir_DefaDpi import Ir_DefaDpi, Ir_DefaObj

class Ir_DefaApi(Ir_DefaDpi):
    async def getRandomId(self):
        w = await self.getAll()
        return random.choice(w)
