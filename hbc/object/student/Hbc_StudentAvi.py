# Пользовательский файл для интерфейса
from .Hbc_StudentDvi import Hbc_StudentDvi
from core.base.BaseOper import SetOper

class Hbc_StudentAvi(Hbc_StudentDvi):
    class List(Hbc_StudentDvi.DviList):
        @SetOper(label='Загрузить')
        async def UploadStudentByGSheet(self):
            from ..Hbc_GSheetsManagerPkg import Hbc_GSheetsManagerPkg
            await Hbc_GSheetsManagerPkg().GetStudents()

        @SetOper(label='Удалить')
        async def delete(self):
            await (await self.thisApi()).delete(await self.thisRop())
            await self.refresh()

        async def openCh(self, master):
            from ..studentdata.Hbc_StudentDataAvi import Hbc_StudentDataAvi
            from ..studentlesson.Hbc_StudentLessonAvi import Hbc_StudentLessonAvi
            await Hbc_StudentDataAvi.List_idStudent().open(master)
            await Hbc_StudentLessonAvi.List_idStudent().open(master)


    class LookUp(Hbc_StudentDvi.DviLookUp):
        pass
