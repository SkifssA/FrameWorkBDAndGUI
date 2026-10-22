# Пользовательский файл для интерфейса
from .Bc_ScriptSchedulerDvi import Bc_ScriptSchedulerDvi
from core.sdk import Form


class Bc_ScriptSchedulerPub(Bc_ScriptSchedulerDvi):
    metaFile = "Bc_ScriptScheduler.Ameta.json"

    class List(Bc_ScriptSchedulerDvi.DviList):
        pass

    class Card(Bc_ScriptSchedulerDvi.DviCard):
        pass

    class TextCard(Bc_ScriptSchedulerDvi.DviCard):
        def onRefresh(self):
            return self.thisLogic().load(self.getAttr('super$id'))

    class LookUp(Bc_ScriptSchedulerDvi.DviLookUp):
        pass

    @classmethod
    def list(cls, **kwargs):
        return Form(cls.List, cls, **kwargs)

    @classmethod
    def card(cls, **kwargs):
        return Form(cls.Card, cls, **kwargs)

    @classmethod
    def textCard(cls, **kwargs):
        return Form(cls.TextCard, cls, **kwargs)
