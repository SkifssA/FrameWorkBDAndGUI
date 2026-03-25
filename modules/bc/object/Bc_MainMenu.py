from core.form.MainMenu import mainMenu
from core.base.oper import SetOper

from ..object.config.Bc_ConfigAvi import Bc_ConfigAvi
from ..object.scriptscheduler.Bc_ScriptSchedulerAvi import Bc_ScriptSchedulerAvi
from ..object.timeline.Bc_TimeLineAvi import Bc_TimeLineAvi
from ..object.icons.Bc_IconsAvi import Bc_IconsAvi

class Bc_MainMenu(mainMenu):
    class Default(mainMenu.Default):
        @SetOper(label="Справочники")
        def mm_jurnal(self): pass

        @SetOper(label='Еденицы времени', order=1, headOper='mm_jurnal')
        def Bc_TimeLine(self):
            Bc_TimeLineAvi.list().param(parent=self).open()

        @SetOper(label='Иконки', order=2, headOper='mm_jurnal')
        def Bc_TimeLine(self):
            Bc_IconsAvi().list().param(parent=self).open()

        @SetOper(label="Настройки", order=1)
        def mm_setting(self): pass

        @SetOper(label='Конфигурация', order=1, headOper='mm_setting')
        def Bc_Config(self):
            Bc_ConfigAvi.list().param(parent=self).open()

        @SetOper(label='Отложеные скритпы', order=2, headOper='mm_setting')
        def Bc_ScriptScheduler(self):
            Bc_ScriptSchedulerAvi.list().param(parent=self).open()
        