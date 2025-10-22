# Пользовательский файл для интерфейса
from .Core_ScriptDvi import Core_ScriptDvi

class Core_ScriptAvi(Core_ScriptDvi):
    class List(Core_ScriptDvi.DviList):
        pass

    class LookUp(Core_ScriptDvi.DviLookUp):
        pass
