# Пользовательский файл для интерфейса
from .Hbc_StudentLessonDvi import Hbc_StudentLessonDvi
from ..student.Hbc_StudentApi import Hbc_StudentApi
from ..Hbc_NewProfiClientPkg import Hbc_NewProfiClientPkg
from core.base.BaseOper import SetOper

class Hbc_StudentLessonAvi(Hbc_StudentLessonDvi):
    class List(Hbc_StudentLessonDvi.DviList):
        showAttr = ['idStudentHL', 'idLessonHL']

        @SetOper(label='Обновить практические', order=-1)
        async def uploadlessonAll(self):
            sHeadLineListt = []
            for i in await Hbc_StudentApi().findBybEnd():
                rop = await Hbc_StudentApi().load(i)
                sHeadLineListt.append(Hbc_StudentApi().calcHeadLine(rop))
            w = Hbc_NewProfiClientPkg()
            await w.Login()
            await w.createFileStudents(sHeadLineListt)
            await self.refresh()

        @SetOper(label='Загрузить файлы по уроку')
        async def uploadlesson(self):
            w = Hbc_NewProfiClientPkg()
            await w.Login()
            await w.uploadFilesAssign(await self.thisRop())

        @SetOper(label='Загрузить файлы по всем урокам')
        async def uploadAlllesson(self):
            w = Hbc_NewProfiClientPkg()
            await w.Login()
            await w.uploadFilesAssign(await self.thisRop())

        @SetOper(label='Оценить')
        async def fillScore(self):
            w = Hbc_NewProfiClientPkg()
            await w.Login()
            await w.fillScore(await self.thisRop())
            await self._refresh()

        # @SetFilter('t.bFillScore is Null or :filter$flt_NotScore = 1')
        # async def flt_NotScore(self):
        #     await self._refresh()

        def checwork(self):
            super().checwork()
            self.selection.oper('fillScore').isDisabled = self.getAttr('bUploadFile') is None

    class List_idStudent(Hbc_StudentLessonDvi.DviList):
        showAttr = ['idLessonHL', 'bUploadFile', 'bFillScore']
        async def onRefresh(self):
            return await super().onRefresh() + f"WHERE t.idStudent = {self.getAttr('super$id')}"
        
        def openCh(self):
            from bc.object.file.Bc_FileAvi import Bc_FileAvi
            yield Bc_FileAvi.list_gidSrc(right=True)

    class LookUp(Hbc_StudentLessonDvi.DviLookUp):
        pass
