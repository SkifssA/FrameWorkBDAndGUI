# Пользовательский файл для интерфейса
from core.sdk import Oper

from .Bc_TimeLineDvi import Bc_TimeLineDvi

class Bc_TimeLinePub(Bc_TimeLineDvi):
    class List(Bc_TimeLineDvi.DviList):
        @Oper(label="Справочник1", order=10)
        def mm_res1(self): pass

        @Oper(label="Справочник2", order=20)
        def mm_res2(self): pass

        @Oper(label="Справочник3", order=30)
        def mm_res3(self): pass

    class Card(Bc_TimeLineDvi.DviCard): pass

    class LookUp(Bc_TimeLineDvi.DviLookUp): pass