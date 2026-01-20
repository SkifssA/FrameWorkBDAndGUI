# Пользовательский файл для интерфейса
from .Hbc_LessonDvi import Hbc_LessonDvi

class Hbc_LessonAvi(Hbc_LessonDvi):
    @classmethod
    def list(cls, **kwargs):
        return cls.typeMeta(cls.List, **kwargs)
    
    @classmethod
    def card(cls, **kwargs):
        return cls.typeMeta(cls.Card, **kwargs)

    class List(Hbc_LessonDvi.DviList): pass

    class Card(Hbc_LessonDvi.DviCard): pass

    class LookUp(Hbc_LessonDvi.DviLookUp): pass
