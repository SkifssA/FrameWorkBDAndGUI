# Пользовательский файл для логики
from .Ir_DefTypeDpi import Ir_DefTypeDpi, Ir_DefTypeObj

class Ir_DefTypeApi(Ir_DefTypeDpi):

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
        await self.register('lite', 'Легкая')
        await self.register('midl', 'Средняя')
