# Пользовательский файл для интерфейса
from .Core_AttrDvi import Core_AttrDvi

class Core_AttrAvi(Core_AttrDvi):
    class List(Core_AttrDvi.DviList):
        pass

    class LookUp(Core_AttrDvi.DviLookUp):
        pass
