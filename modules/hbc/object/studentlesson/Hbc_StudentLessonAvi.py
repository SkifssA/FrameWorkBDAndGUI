# Пользовательский файл для интерфейса
from .Hbc_StudentLessonDvi import Hbc_StudentLessonDvi
from ..Hbc_NewProfiClientPkg import Hbc_NewProfiClientPkg
from ..student.Hbc_StudentApi import Hbc_StudentApi
from core.base.oper import SetOper
from core.formhandle.FornManeger import FormHandle, FornManeger

class Hbc_StudentLessonAvi(Hbc_StudentLessonDvi):
    class List(Hbc_StudentLessonDvi.DviList):
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

        @SetOper(label='Оценить')
        async def fillScore(self):
            w = Hbc_NewProfiClientPkg()
            await w.Login()
            await w.fillScore(await self.thisRop())
            await self.refresh()

        # @SetFilter('t.bFillScore is Null or :filter$flt_NotScore = 1')
        # async def flt_NotScore(self):
        #     await self.refresh()

        def checwork(self):
            super().checwork()
            self.selection.oper('fillScore').isDisabled = self.getAttr('bUploadFile') is None

    class List_idStudent(Hbc_StudentLessonDvi.DviList):
        def onRefresh(self):
            return super().onRefresh() + f"WHERE t.idStudent = :super$id"
        
        def openCh(self):
            from modules.bc.object.file.Bc_FileAvi import Bc_FileAvi
            yield Bc_FileAvi.list_gidSrc().param(locat='right')

        def refreshCh(self):
            return super().refreshCh()

    class Card(Hbc_StudentLessonDvi.DviCard): pass

    class LookUp(Hbc_StudentLessonDvi.DviLookUp): pass

    @classmethod
    def list(cls)->FormHandle:
        return FornManeger.register(cls.List)
    
    @classmethod
    def card(cls)->FormHandle:
        return FornManeger.register(cls.Card)
    
    @classmethod
    def list_idStudent(cls)->FormHandle:
        return FornManeger.register(cls.List_idStudent)
