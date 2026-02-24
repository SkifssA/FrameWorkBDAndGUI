# Пользовательский файл для логики
from .Ir_RareDpi import Ir_RareDpi, Ir_RareObj

class Ir_RareApi(Ir_RareDpi):
    async def register(self, sCode: str, sCaption: str, sColor: str):
        id = await self.findByMnemocode(sCode)
        if id is None:
            obj = await self.insert()
            self.setsCode(obj, sCode)
        else:
            obj = await self.load(id)

        self.setsColor(obj, sColor)
        self.setsCaption(obj, sCaption)

        await self.update(obj)

    async def dataInstall(self):
        await self.register("Basic", "Обычный", "#FFFFFF")
        await self.register("Uncommon", "Необычный", "#1EFF00")
        await self.register("Rare", "Редкий", "#0070DD")
        await self.register("Epic", "Эпический", "#A335EE")
        await self.register("Legendary", "Легендарный", "#FF8000")
