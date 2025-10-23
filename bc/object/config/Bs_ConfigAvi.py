# Пользовательский файл для интерфейса
from .Bs_ConfigDvi import Bs_ConfigDvi

class Bs_ConfigAvi(Bs_ConfigDvi):
    class List(Bs_ConfigDvi.DviList):
        pass

    class LookUp(Bs_ConfigDvi.DviLookUp):
        pass
