# Пользовательский файл для логики
from .Ir_WeaponTypeDpi import Ir_WeaponTypeDpi, Ir_WeaponTypeObj

class Ir_WeaponTypeApi(Ir_WeaponTypeDpi):

    async def register(self, sCode: str, sCaption: str):
        id = await self.findByMnemocode(sCode)
        if id is None:
            obj = await self.insert()
            self.setsCode(obj, sCode)
        else:
            obj = await self.load(id)

        self.setsCaption(obj, sCaption)

        await self.update(obj)

    async def dataInstall(self):
        await self.register('sword', 'Меч')
        await self.register('bow', 'Лук')
