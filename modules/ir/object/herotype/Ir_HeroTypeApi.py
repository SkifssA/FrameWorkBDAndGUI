# Пользовательский файл для логики
from .Ir_HeroTypeDpi import Ir_HeroTypeDpi, Ir_HeroTypeObj
from ..weapontype.Ir_WeaponTypeApi import Ir_WeaponTypeApi
from ..deftype.Ir_DefTypeApi import Ir_DefTypeApi

class Ir_HeroTypeApi(Ir_HeroTypeDpi):
    async def register(self, sCode: str, sCaption: str, idWeaponType: int, idDefType: int):
        id = await self.findByMnemocode(sCode)
        if id is None:
            obj = await self.insert()
            self.setsCode(obj, sCode)
        else:
            obj = await self.load(id)

        self.setidWeaponType(obj, idWeaponType)
        self.setidDefType(obj, idDefType)
        self.setsCaption(obj, sCaption)

        await self.update(obj)

    async def dataInstall(self):
        await self.register('Warrior', 'Воин', await Ir_WeaponTypeApi().findByMnemocode('sword'), await Ir_DefTypeApi().findByMnemocode('midl'))
        await self.register('Archer', 'Лучник', await Ir_WeaponTypeApi().findByMnemocode('bow'), await Ir_DefTypeApi().findByMnemocode('lite'))
