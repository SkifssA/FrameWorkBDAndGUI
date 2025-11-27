# Пользовательский файл для интерфейса
from .Hbc_StudentDataDvi import Hbc_StudentDataDvi

class Hbc_StudentDataAvi(Hbc_StudentDataDvi):
    class List(Hbc_StudentDataDvi.DviList): pass

    class List_idStudent(Hbc_StudentDataDvi.DviList): 
        showAttr = ['sData']
        async def onRefresh(self):
            return f"""
            SELECT t.id,
                   t.gid,
                   t.idStudent,
                   t1.sHeadLine as idStudentHL,
                   t.sData
            FROM Hbc_StudentData AS t
                   LEFT JOIN Hbc_Student t1 ON t1.id = t.idStudent
            WHERE t.idStudent = {self.getAttr('super$id')}
            """

    class LookUp(Hbc_StudentDataDvi.DviLookUp): pass
