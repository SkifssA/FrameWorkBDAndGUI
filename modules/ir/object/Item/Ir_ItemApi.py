# Пользовательский файл для логики
from .Ir_ItemDpi import Ir_ItemDpi, Ir_ItemObj
from modules.ir.object.Itemloot.Ir_ItemLootApi import Ir_ItemLootApi
from modules.ir.object.defa.Ir_DefaApi import Ir_DefaApi
from modules.ir.object.weapon.Ir_WeaponApi import Ir_WeaponApi

class Ir_ItemApi(Ir_ItemDpi):
    async def insertByItem(self, gidItem):
        obj = await self.insert()
        self.setgidScr(obj, gidItem)
        await self.update(obj)

    def calcHeadLine(self, rop):
        apiDict = {
            self.asyncRun(Ir_ItemLootApi().idClass()): Ir_ItemLootApi 
            , self.asyncRun(Ir_DefaApi().idClass()): Ir_DefaApi 
            , self.asyncRun(Ir_WeaponApi().idClass()): Ir_WeaponApi 
        }
        
        api = apiDict[rop.gidScr.getIdClass()]()

        obj = self.asyncRun(api.load(rop.gidScr.getId()))
        return api.calcHeadLine(obj)
