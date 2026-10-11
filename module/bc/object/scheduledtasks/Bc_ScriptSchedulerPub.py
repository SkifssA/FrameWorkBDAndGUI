# Пользовательский файл для интерфейса
from .Bc_ScriptSchedulerDvi import Bc_ScriptSchedulerDvi
from core.sdk import Form


class Bc_ScriptSchedulerPub(Bc_ScriptSchedulerDvi):
    metaFile = "Bc_ScriptScheduler.Ameta.json"

    class List(Bc_ScriptSchedulerDvi.DviList):
        pass

    class Card(Bc_ScriptSchedulerDvi.DviCard):
        pass

    class LookUp(Bc_ScriptSchedulerDvi.DviLookUp):
        pass

    @classmethod
    def list(cls):
        return Form(cls.List, cls)

    @classmethod
    def card(cls):
        return Form(cls.Card, cls)
