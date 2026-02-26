# Пользовательский файл для логики
import random

from .Ir_ItemLootDpi import Ir_ItemLootDpi, Ir_ItemLootObj

class Ir_ItemLootApi(Ir_ItemLootDpi):
    async def getRandomId(self):
        w = await self.getAll()
        return random.choice(w)
