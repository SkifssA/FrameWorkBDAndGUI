# Пользовательский файл для логики
from .Ir_ItemDpi import Ir_ItemDpi, Ir_ItemObj

class Ir_ItemApi(Ir_ItemDpi):
    async def insertByItem(self, gidItem):
        obj = await self.insert()
        self.setgidScr(obj, gidItem)
        await self.update(obj)
