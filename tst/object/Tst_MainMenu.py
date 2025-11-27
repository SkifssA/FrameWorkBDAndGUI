from core.base.BaseOper import SetOper
from core.base.BaseMainMenu import mainMenu

from ..object.test.Tst_TestAvi import Tst_TestAvi

class Tst_MainMenu(mainMenu):
    @SetOper(label="Справочники")
    def mm_respo(self): pass

    @SetOper(label='Разнообразный класс', order=1, headOper='mm_respo')
    async def Hbc_Lesson(self):
        await Tst_TestAvi.List().open()