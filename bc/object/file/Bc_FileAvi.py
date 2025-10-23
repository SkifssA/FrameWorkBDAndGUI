# Пользовательский файл для интерфейса
from .Bc_FileDvi import Bc_FileDvi

class Bc_FileAvi(Bc_FileDvi):
    class List(Bc_FileDvi.DviList):
        pass

    class LookUp(Bc_FileDvi.DviLookUp):
        pass
