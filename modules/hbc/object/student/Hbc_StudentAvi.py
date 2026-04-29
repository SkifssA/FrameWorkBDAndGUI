# Пользовательский файл для интерфейса
from .Hbc_StudentDvi import Hbc_StudentDvi
from engine.base.oper import SetOper

class Hbc_StudentAvi(Hbc_StudentDvi):
    @classmethod
    def list(cls, **kwargs):
        return cls.typeMeta(cls.List, **kwargs)

    @classmethod
    def card(cls, **kwargs):
        return cls.typeMeta(cls.Card, **kwargs)

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

    class LookUp(Hbc_StudentDvi.DviLookUp): pass

    class LookUp(Hbc_StudentDvi.DviLookUp):
        pass
