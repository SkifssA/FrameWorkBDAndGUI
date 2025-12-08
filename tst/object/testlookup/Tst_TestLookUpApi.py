# Пользовательский файл для логики
from .Tst_TestLookUpDpi import Tst_TestLookUpDpi, Tst_TestLookUpObj

class Tst_TestLookUpApi(Tst_TestLookUpDpi):
    async def dataInstall(self):
        await self.create("Облако")
        await self.create("Ключ")
        await self.create("Мост")
        

    async def create(self, sName):
        r = await self.insert()
        r.sName = sName
        await self.update(r)
