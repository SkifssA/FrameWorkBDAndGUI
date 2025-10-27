from . import Hbc_LessonAvi, Hbc_StudentAvi, Hbc_StudentDataAvi, Hbc_StudentLessonAvi
from core.base.BaseOper import SetOper
from core.base.BaseMainMenu import mainMenu

class Hbc_MainMenu(mainMenu):
    @SetOper(label="Справочники")
    def mm_respo(self): pass

    @SetOper(label='Уроки', order=1, headOper='mm_respo')
    async def Hbc_Lesson(self):
        await Hbc_LessonAvi.List().open()

    @SetOper(label="Ученики")
    def mm_student(self):pass

    @SetOper(label='Ученики', order=2, headOper="mm_student")
    async def Hbc_Student(self):
        await Hbc_StudentAvi.List().open()

    @SetOper(label='Время учеников', order=3, headOper="mm_student")
    async def Hbc_StudentData(self):
        await Hbc_StudentDataAvi.List().open()

    @SetOper(label='Выполненые практические', order=4, headOper="mm_student")
    async def Hbc_StudentLesson(self):
        await Hbc_StudentLessonAvi.List().open()