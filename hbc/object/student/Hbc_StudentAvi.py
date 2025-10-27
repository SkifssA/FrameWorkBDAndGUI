# Пользовательский файл для интерфейса
from .Hbc_StudentDvi import Hbc_StudentDvi

class Hbc_StudentAvi(Hbc_StudentDvi):
    class List(Hbc_StudentDvi.DviList):
        pass
        # @SetButton(label='Загрузить', isLong=True)
        # async def UploadStudentByGSheet(self, update_progress):
        #     from ..Hbc_GSheetsManagerPkg import Hbc_GSheetsManagerPkg
        #     await Hbc_GSheetsManagerPkg().GetStudents()

        # @SetButton(label='Удалить', isLong=True)
        # async def delete(self, update_progress):
        #     await (await self.thisApi()).delete(await self.thisRop())


    class LookUp(Hbc_StudentDvi.DviLookUp):
        pass
