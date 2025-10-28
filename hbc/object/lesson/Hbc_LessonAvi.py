# Пользовательский файл для интерфейса
from .Hbc_LessonDvi import Hbc_LessonDvi
from core.base.BaseOper import SetOper

class Hbc_LessonAvi(Hbc_LessonDvi):
    class List(Hbc_LessonDvi.DviList):
        showAttr = ['sCaption']

    class LookUp(Hbc_LessonDvi.DviLookUp):
        pass
