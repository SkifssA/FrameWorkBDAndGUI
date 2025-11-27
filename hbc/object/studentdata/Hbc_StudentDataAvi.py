# Пользовательский файл для интерфейса
from .Hbc_StudentDataDvi import Hbc_StudentDataDvi

class Hbc_StudentDataAvi(Hbc_StudentDataDvi):
    class List(Hbc_StudentDataDvi.DviList): pass

    class List_idStudent(Hbc_StudentDataDvi.DviList):
        async def onRefresh(self):
            return await super().onRefresh() + f"WHERE t.idStudent = {self.getAttr('super$id')}"

    class LookUp(Hbc_StudentDataDvi.DviLookUp): pass
