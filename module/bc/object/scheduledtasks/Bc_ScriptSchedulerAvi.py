# Пользовательский файл для интерфейса
from .Bc_ScriptSchedulerDvi import Bc_ScriptSchedulerDvi

class Bc_ScriptSchedulerAvi(Bc_ScriptSchedulerDvi):
    class List(Bc_ScriptSchedulerDvi.DviList): pass

    class Card(Bc_ScriptSchedulerDvi.DviCard): pass

    class LookUp(Bc_ScriptSchedulerDvi.DviLookUp): pass
