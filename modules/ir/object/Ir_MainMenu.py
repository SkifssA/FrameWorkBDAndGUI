from core.base.BaseMainMenu import mainMenu
from core.base.BaseOper import SetOper

from .hero.Ir_HeroAvi import Ir_HeroAvi
from .defa.Ir_DefaAvi import Ir_DefaAvi
from .weapon.Ir_WeaponAvi import Ir_WeaponAvi

class Ir_MainMenu(mainMenu):
    @SetOper(label="Справочники")
    def mm_respo(self): pass
        
    @SetOper(label='Герои', order=1, headOper='mm_respo')
    async def Ir_Hero(self):
        await Ir_HeroAvi.List().open()

    @SetOper(label='Оружие', order=2, headOper='mm_respo')
    async def Ir_Weapon(self):
        await Ir_WeaponAvi.List().open()

    @SetOper(label='Броня', order=3, headOper='mm_respo')
    async def Ir_Defa(self):
        await Ir_DefaAvi.List().open()