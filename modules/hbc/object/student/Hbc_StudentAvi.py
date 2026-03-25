# Пользовательский файл для интерфейса
from .Hbc_StudentDvi import Hbc_StudentDvi
from core.base.oper import SetOper
from core.formhandle.FornManeger import FormHandle, FornManeger

class Hbc_StudentAvi(Hbc_StudentDvi):
    class List(Hbc_StudentDvi.DviList):
        @SetOper(label='Загрузить')
        async def UploadStudentByGSheet(self):
            from ..Hbc_GSheetsManagerPkg import Hbc_GSheetsManagerPkg
            await Hbc_GSheetsManagerPkg().GetStudents()

        def openCh(self):
            from ..studentdata.Hbc_StudentDataAvi import Hbc_StudentDataAvi
            from ..studentlesson.Hbc_StudentLessonAvi import Hbc_StudentLessonAvi
            yield Hbc_StudentDataAvi.list_idStudent()
            yield Hbc_StudentLessonAvi.list_idStudent()

    class Card (Hbc_StudentDvi.DefaultCard): pass

    class LookUp(Hbc_StudentDvi.DviLookUp): pass

    @classmethod
    def list(cls)->FormHandle:
        return FornManeger.register(cls.List)
    
    @classmethod
    def card(cls)->FormHandle:
        return FornManeger.register(cls.Card)
