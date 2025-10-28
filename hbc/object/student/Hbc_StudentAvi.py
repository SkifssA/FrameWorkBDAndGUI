# Пользовательский файл для интерфейса
from .Hbc_StudentDvi import Hbc_StudentDvi
from core.base.BaseOper import SetOper

class Hbc_StudentAvi(Hbc_StudentDvi):
    class List(Hbc_StudentDvi.DviList):
        pass
        @SetOper(label='Загрузить')
        async def UploadStudentByGSheet(self):
            from ..Hbc_GSheetsManagerPkg import Hbc_GSheetsManagerPkg
            await Hbc_GSheetsManagerPkg().GetStudents()

        # @SetButton(label='Удалить', isLong=True)
        # async def delete(self, update_progress):
        #     await (await self.thisApi()).delete(await self.thisRop())


    class LookUp(Hbc_StudentDvi.DviLookUp):
        pass
