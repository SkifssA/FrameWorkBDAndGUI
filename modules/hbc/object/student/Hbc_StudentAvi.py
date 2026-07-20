# Пользовательский файл для интерфейса
from .Hbc_StudentDvi import Hbc_StudentDvi
from engine.base.oper import SetOper
from engine.fabric.Form import FormConstruct

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

    class Card(Hbc_StudentDvi.DviCard): pass

    class LookUp(Hbc_StudentDvi.DviLookUp): pass

    @classmethod
    def list(cls)->FormConstruct:
        return FormConstruct(cls.List)
    
    @classmethod
    def card(cls)->FormConstruct:
        return FormConstruct(cls.Card)
    
    @classmethod
    def lookUp(cls)->FormConstruct:
        return FormConstruct(cls.LookUp)
