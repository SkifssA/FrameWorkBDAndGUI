# Пользовательский файл для интерфейса
from .Bc_TimeLineDvi import Bc_TimeLineDvi
from core.sdk import Form, Oper, Setter


class Bc_TimeLinePub(Bc_TimeLineDvi):
    metaFile = "Bc_TimeLine.Ameta.json"

    class List(Bc_TimeLineDvi.DviList):
        @Oper(label="Справочник1", order=10)
        def mm_res1(self):
            pass

        @Oper(label="Справочник2", order=20)
        def mm_res2(self):
            pass

        @Oper(label="Справочник3", order=30)
        def mm_res3(self):
            pass

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
