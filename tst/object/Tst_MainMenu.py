from core.base.BaseOper import SetOper
from core.base.BaseMainMenu import mainMenu

from ..object.test.Tst_TestAvi import Tst_TestAvi
from ..object.testlookup.Tst_TestLookUpAvi import Tst_TestLookUpAvi

class Tst_MainMenu(mainMenu):
    @SetOper(label="Справочники")
    def mm_respo(self): pass

    @SetOper(label='Разнообразный класс', order=1, headOper='mm_respo')
    async def mm_Tst_Test(self):
        await Tst_TestAvi.list().open()

    @SetOper(label='Выподающий список', order=1, headOper='mm_respo')
    async def mm_Tst_TestLookUpAvi(self):
        await Tst_TestLookUpAvi.list().open()