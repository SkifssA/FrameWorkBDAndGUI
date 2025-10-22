# Пользовательский файл для интерфейса
from .Core_ClassDvi import Core_ClassDvi

class Core_ClassAvi(Core_ClassDvi):
    class List(Core_ClassDvi.DviList):
        pass

    class LookUp(Core_ClassDvi.DviLookUp):
        pass
