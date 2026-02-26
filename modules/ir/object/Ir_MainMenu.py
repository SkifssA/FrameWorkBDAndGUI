from core.empty.BaseMainMenu import mainMenu
from core.base.BaseOper import SetOper

from modules.bc.object.log.Bc_LogAvi import Bc_LogAvi

from .hero.Ir_HeroAvi import Ir_HeroAvi
from .defa.Ir_DefaAvi import Ir_DefaAvi
from .weapon.Ir_WeaponAvi import Ir_WeaponAvi
from .Itemloot.Ir_ItemLootAvi import Ir_ItemLootAvi

from modules.bc.object.log.Bc_LogAvi import Bc_LogAvi

class Ir_MainMenu(mainMenu):
    class Default(mainMenu.Default):
        async def firstFrame(self):
            await Bc_LogAvi.list().open(parent="main_window")

        def openCh(self):
            yield  Bc_LogAvi.list()

        @SetOper(label="Справочники")
        def mm_respo(self): pass
            
        @SetOper(label='Герои', order=1, headOper='mm_respo')
        async def Ir_Hero(self):
            await Ir_HeroAvi.list().open()

        @SetOper(label='Оружие', order=2, headOper='mm_respo')
        async def Ir_Weapon(self):
            await Ir_WeaponAvi.list().open()

        @SetOper(label='Броня', order=3, headOper='mm_respo')
        async def Ir_Defa(self):
            await Ir_DefaAvi.list().open()

        @SetOper(label='Предметы', order=4, headOper='mm_respo')
        async def Ir_ItemLootAvi(self):
            await Ir_ItemLootAvi.list().open()