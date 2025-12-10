# Пользовательский файл для интерфейса
from .Tst_TestDvi import Tst_TestDvi
from core.base.BaseOper import SetOper

class Tst_TestAvi(Tst_TestDvi):
    @classmethod
    def list(cls, **kwargs):
        return cls.typeMeta(cls.List, **kwargs)
    
    @classmethod
    def card(cls, **kwargs):
        return cls.typeMeta(cls.Card, **kwargs)
    
    class List(Tst_TestDvi.DviList):pass

    class Card(Tst_TestDvi.DviCard): pass

    class LookUp(Tst_TestDvi.DviLookUp): pass
