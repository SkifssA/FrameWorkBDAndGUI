# Пользовательский файл для интерфейса
from .Bc_TimeLineDvi import Bc_TimeLineDvi
from module.bc.object.scheduledtasks.Bc_ScriptSchedulerPub import Bc_ScriptSchedulerPub
from core.sdk import Form, Oper, Setter


class Bc_TimeLinePub(Bc_TimeLineDvi):
    metaFile = "Bc_TimeLine.Ameta.json"

    class List(Bc_TimeLineDvi.DviList):
        @Oper(label="Открыть карточку", order=30)
        def mm_res1(self):
            Bc_TimeLinePub.card().param('idItem', self.getAttr('id')).open()

        @Setter
        def setsCaption(self):
            pass

    class Card(Bc_TimeLineDvi.DviCard):
        pass

    class LookUp(Bc_TimeLineDvi.DviLookUp):
        pass

    @classmethod
    def list(cls):
        return Form(cls.List, cls)

    @classmethod
    def card(cls):
        return Form(cls.Card, cls)
