from engine.form.MainMenu import mainMenu
from engine.base.oper import SetOper

from modules.gmb import Gmb_TaskAvi

class Gmb_MainMenu(mainMenu):
    class Default(mainMenu.Default):
        def firstFrame(self):
            return Gmb_TaskAvi.list()

        @SetOper(label="Справочники")
        def mm_respo(self): pass

        @SetOper(label='Задачи', order=1, headOper='mm_respo')
        async def Awh_Anime(self):
            Gmb_TaskAvi.list().open()
        