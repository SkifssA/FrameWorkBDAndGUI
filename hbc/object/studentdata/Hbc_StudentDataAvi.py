# Пользовательский файл для интерфейса
from .Hbc_StudentDataDvi import Hbc_StudentDataDvi

class Hbc_StudentDataAvi(Hbc_StudentDataDvi):
    class List(Hbc_StudentDataDvi.DviList):
        pass

    class LookUp(Hbc_StudentDataDvi.DviLookUp):
        pass
