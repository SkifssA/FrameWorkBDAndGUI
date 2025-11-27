# Пользовательский файл для интерфейса
from .Tst_TestDvi import Tst_TestDvi
from core.base.BaseOper import SetOper

class Tst_TestAvi(Tst_TestDvi):
    class List(Tst_TestDvi.DviList):

        @SetOper(label='Открыть карточку')
        async def fillScore(self):
            await Tst_TestAvi.Card().open()

    class Card(Tst_TestDvi.DviCard): pass

    class LookUp(Tst_TestDvi.DviLookUp): pass
