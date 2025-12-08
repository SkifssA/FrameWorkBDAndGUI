# Пользовательский файл для интерфейса
from .Tst_TestLookUpDvi import Tst_TestLookUpDvi

class Tst_TestLookUpAvi(Tst_TestLookUpDvi):
    class List(Tst_TestLookUpDvi.DviList):
        pass

    class LookUp(Tst_TestLookUpDvi.DviLookUp):
        pass
