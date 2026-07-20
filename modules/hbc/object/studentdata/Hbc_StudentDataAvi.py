# Пользовательский файл для интерфейса
from .Hbc_StudentDataDvi import Hbc_StudentDataDvi
from engine.fabric.Form import FormConstruct

class Hbc_StudentDataAvi(Hbc_StudentDataDvi):   
    class List(Hbc_StudentDataDvi.DviList): pass

    class List_idStudent(Hbc_StudentDataDvi.DviList):
        def onRefresh(self):
            return super().onRefresh() + "WHERE t.idStudent = :super$id"

    class Card(Hbc_StudentDataDvi.DviCard): pass

    class LookUp(Hbc_StudentDataDvi.DviLookUp): pass

    @classmethod
    def list(cls)->FormConstruct:
        return FormConstruct(cls.List)
    
    @classmethod
    def list_idStudent(cls)->FormConstruct:
        return FormConstruct(cls.List_idStudent)
    
    @classmethod
    def card(cls)->FormConstruct:
        return FormConstruct(cls.Card)