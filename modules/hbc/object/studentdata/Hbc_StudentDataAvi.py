# Пользовательский файл для интерфейса
from .Hbc_StudentDataDvi import Hbc_StudentDataDvi

class Hbc_StudentDataAvi(Hbc_StudentDataDvi):   
    class List(Hbc_StudentDataDvi.DviList): pass

    class List_idStudent(Hbc_StudentDataDvi.DviList):
        async def onRefresh(self):
            return await super().onRefresh() + f"WHERE t.idStudent = :super$id"

    class Card(Hbc_StudentDataDvi.DviCard): pass

    class LookUp(Hbc_StudentDataDvi.DviLookUp): pass

    @classmethod
    def list(cls, **kwargs)->List:
        return cls.typeMeta(cls.List, **kwargs)
    
    @classmethod
    def card(cls, **kwargs)->Card:
        return cls.typeMeta(cls.Card, **kwargs)

    @classmethod
    def list_idStudent(cls, **kwargs)->List_idStudent:
        return cls.typeMeta(cls.List_idStudent, **kwargs)
