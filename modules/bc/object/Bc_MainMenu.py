from core.base.BaseMainMenu import mainMenu
from core.base.BaseOper import SetOper

from ..object.config.Bc_ConfigAvi import Bc_ConfigAvi
from ..object.scriptscheduler.Bc_ScriptSchedulerAvi import Bc_ScriptSchedulerAvi
from ..object.timeline.Bc_TimeLineAvi import Bc_TimeLineAvi
from ..object.icons.Bc_IconsAvi import Bc_IconsAvi

class Bc_MainMenu(mainMenu):

    @SetOper(label="Справочники")
    def mm_jurnal(self): pass

    @SetOper(label='Еденицы времени', order=1, headOper='mm_jurnal')
    async def Bc_TimeLine(self):
        await Bc_TimeLineAvi.list().open()

    @SetOper(label='Иконки', order=2, headOper='mm_jurnal')
    async def Bc_TimeLine(self):
        await Bc_IconsAvi().list().open()

    @SetOper(label="Настройки", order=1)
    def mm_setting(self): pass

    @SetOper(label='Конфигурация', order=1, headOper='mm_setting')
    async def Bc_Config(self):
        await Bc_ConfigAvi.list().open()

    @SetOper(label='Отложеные скритпы', order=2, headOper='mm_setting')
    async def Bc_ScriptScheduler(self):
        await Bc_ScriptSchedulerAvi.list().open()
        