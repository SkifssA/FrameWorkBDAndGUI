from engine.form.MainMenu import mainMenu
from engine.base.oper import SetOper

from modules.gmb.object.task.Gmb_TaskAvi import Gmb_TaskAvi
from modules.gmb.object.mod.Gmb_ModAvi import Gmb_ModAvi

class Gmb_MainMenu(mainMenu):
    class Default(mainMenu.Default):
        def firstFrame(self):
            return Gmb_TaskAvi.list()

        @SetOper(label="Справочники")
        def mm_respo(self): pass

        @SetOper(label='Задачи', order=1, headOper='mm_respo')
        async def Gmb_Task(self):
            Gmb_TaskAvi.list().open()

        @SetOper(label='Репозитории', order=2, headOper='mm_respo')
        async def Gmb_Mod(self):
            Gmb_ModAvi.list().open()
        