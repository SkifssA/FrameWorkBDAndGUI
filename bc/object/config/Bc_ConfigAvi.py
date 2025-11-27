# Пользовательский файл для интерфейса
from .Bc_ConfigDvi import Bc_ConfigDvi

class Bc_ConfigAvi(Bc_ConfigDvi):
    class List(Bc_ConfigDvi.DviList):
        pass

    class LookUp(Bc_ConfigDvi.DviLookUp):
        pass
