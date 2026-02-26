# Пользовательский файл для логики
import random

from .Ir_WeaponDpi import Ir_WeaponDpi, Ir_WeaponObj

class Ir_WeaponApi(Ir_WeaponDpi):
    async def getRandomId(self):
        w = await self.getAll()
        return random.choice(w)

