# Пользовательский файл для интерфейса
from .Hbc_LessonDvi import Hbc_LessonDvi
from engine.fabric.Form import FormConstruct

class Hbc_LessonAvi(Hbc_LessonDvi):
    class List(Hbc_LessonDvi.DviList): pass

    class Card(Hbc_LessonDvi.DviCard): pass

    class LookUp(Hbc_LessonDvi.DviLookUp): pass

    @classmethod
    def list(cls)->FormConstruct:
        return FormConstruct(cls.List)
    
    @classmethod
    def card(cls)->FormConstruct:
        return FormConstruct(cls.Card)
