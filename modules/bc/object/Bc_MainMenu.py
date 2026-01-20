from core.base.BaseMainMenu import mainMenu
from core.base.BaseOper import SetOper

from ..object.config.Bc_ConfigAvi import Bc_ConfigAvi
from ..object.scriptscheduler.Bc_ScriptSchedulerAvi import Bc_ScriptSchedulerAvi

class Bc_MainMenu(mainMenu):
    @SetOper(label="Справочники")
    def mm_respo(self): pass

    @SetOper(label='Конфигурация', order=1, headOper='mm_respo')
    async def Bc_Config(self):
        await Bc_ConfigAvi.list().open()

    @SetOper(label='Отложеные скритпы', order=2, headOper='mm_respo')
    async def Bc_ScriptScheduler(self):
        await Bc_ScriptSchedulerAvi.list().open()
        