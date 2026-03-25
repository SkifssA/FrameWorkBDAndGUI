# Пользовательский файл для интерфейса
from .Hbc_StudentDataDvi import Hbc_StudentDataDvi

from core.formhandle.FornManeger import FormHandle, FornManeger

class Hbc_StudentDataAvi(Hbc_StudentDataDvi):   
    class List(Hbc_StudentDataDvi.DviList): pass

    class List_idStudent(Hbc_StudentDataDvi.DviList):
        def onRefresh(self):
            return super().onRefresh() + f"WHERE t.idStudent = :super$id"

    class Card(Hbc_StudentDataDvi.DviCard): pass

    class LookUp(Hbc_StudentDataDvi.DviLookUp): pass

    @classmethod
    def list(cls)->FormHandle:
        return FornManeger.register(cls.List)
    
    @classmethod
    def card(cls)->FormHandle:
        return FornManeger.register(cls.Card)

    @classmethod
    def list_idStudent(cls)->FormHandle:
        return FornManeger.register(cls.List_idStudent)
