# Пользовательский файл для интерфейса
from .Hbc_LessonDvi import Hbc_LessonDvi

class Hbc_LessonAvi(Hbc_LessonDvi):
    class List(Hbc_LessonDvi.DviList):
        showAttr = ['sCaption']
        pass

    class LookUp(Hbc_LessonDvi.DviLookUp):
        pass
