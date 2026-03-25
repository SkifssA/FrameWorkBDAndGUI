# Пользовательский файл для интерфейса
from .Hbc_LessonDvi import Hbc_LessonDvi

from core.formhandle.FornManeger import FormHandle, FornManeger

class Hbc_LessonAvi(Hbc_LessonDvi):
    class List(Hbc_LessonDvi.DviList): pass

    class Card(Hbc_LessonDvi.DviCard): pass

    class LookUp(Hbc_LessonDvi.DviLookUp): pass

    @classmethod
    def list(cls)->FormHandle:
        return FornManeger.register(cls.List)
    
    @classmethod
    def card(cls)->FormHandle:
        return FornManeger.register(cls.Card)
