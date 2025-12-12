# Пользовательский файл для интерфейса
from .Tst_TestLookUpDvi import Tst_TestLookUpDvi

class Tst_TestLookUpAvi(Tst_TestLookUpDvi):
    @classmethod
    def list(cls, **kwargs):
        return cls.typeMeta(cls.List, **kwargs)
    
    @classmethod
    def card(cls, **kwargs):
        return cls.typeMeta(cls.Card, **kwargs)
    
    class List(Tst_TestLookUpDvi.DviList):pass

    class Card(Tst_TestLookUpDvi.DviCard): pass

    class LookUp(Tst_TestLookUpDvi.DviLookUp): pass
