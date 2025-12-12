from core.base.BaseMainMenu import mainMenu
from core.base.BaseOper import SetOper

from ..object.config.Bc_ConfigAvi import Bc_ConfigAvi

class Bc_MainMenu(mainMenu):
    @SetOper(label="Справочники")
    def mm_respo(self): pass

    @SetOper(label='Конфигурация', order=1, headOper='mm_respo')
    async def Hbc_Lesson(self):
        await Bc_ConfigAvi.list().open()