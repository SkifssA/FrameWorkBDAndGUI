# Пользовательский файл для интерфейса
from .Hbc_StudentLessonDvi import Hbc_StudentLessonDvi
from ..student.Hbc_StudentApi import Hbc_StudentApi
from ..Hbc_NewProfiClientPkg import Hbc_NewProfiClientPkg

class Hbc_StudentLessonAvi(Hbc_StudentLessonDvi):
    class List(Hbc_StudentLessonDvi.DviList):
        pass
        # @SetButton(label='Обновить практические', isLong=True)
        # async def uploadlessonAll(self, update_progress):
        #     sHeadLineListt = []
        #     for i in await Hbc_StudentApi().findBybEnd():
        #         rop = await Hbc_StudentApi().load(i)
        #         sHeadLineListt.append(Hbc_StudentApi().calcHeadLine(rop))
        #     w = Hbc_NewProfiClientPkg()
        #     await w.Login()
        #     await w.createFileStudents(sHeadLineListt, update_progress)

        # @SetButton(label='Загрузки')
        # async def upload(self): pass

        # @SetButton(label='Загрузить файлы по уроку', isLong=True, nameMaster='upload')
        # async def uploadlesson(self, update_progress):
        #     update_progress(f'Скачиваю файлы по уроку {self.getAttr('idLessonHL')} ')
        #     w = Hbc_NewProfiClientPkg()
        #     await w.Login()
        #     await w.uploadFilesAssign(await self.thisRop())

        # @SetButton(label='Загрузить файлы по всем урокам', isLong=True, nameMaster='upload')
        # async def uploadAlllesson(self, update_progress):
        #     update_progress(f'ТЕСТ')
        #     w = Hbc_NewProfiClientPkg()
        #     await w.Login()
        #     await w.uploadFilesAssign(await self.thisRop())

        # @SetButton(label='Оценить')
        # async def fillScore(self):
        #     w = Hbc_NewProfiClientPkg()
        #     await w.Login()
        #     await w.fillScore(await self.thisRop())
        #     await self._refresh()

        # @SetFilter('t.bFillScore is Null or :filter$flt_NotScore = 1')
        # async def flt_NotScore(self):
        #     await self._refresh()

        # async def chr(self):
        #     await super().chr()
            
        #     self.oper('fillScore').isDisabled = self.getAttr('bUploadFile') is None

    class LookUp(Hbc_StudentLessonDvi.DviLookUp):
        pass
