from .lesson.Hbc_LessonAvi import Hbc_LessonAvi
from .student.Hbc_StudentAvi import Hbc_StudentAvi
from .studentdata.Hbc_StudentDataAvi import Hbc_StudentDataAvi
from .studentlesson.Hbc_StudentLessonAvi import Hbc_StudentLessonAvi
from core.base.oper import SetOper
from core.empty.MainMenu import mainMenu
from modules.bc.object.file.Bc_FileAvi import Bc_FileAvi

class Hbc_MainMenu(mainMenu):
    class Default(mainMenu.Default):
        @SetOper(label="Справочники")
        def mm_respo(self): pass

        @SetOper(label='Уроки', order=1, headOper='mm_respo')
        async def Hbc_Lesson(self):
            await Hbc_LessonAvi.List().open(parent=self.locationsChildrens['bottom'])

        @SetOper(label='Файлы', order=2, headOper='mm_respo')
        async def Bc_File(self):
            await Bc_FileAvi.List().open(parent=self.locationsChildrens['bottom'])

        @SetOper(label="Ученики")
        def mm_student(self):pass

        @SetOper(label='Ученики', order=1, headOper="mm_student")
        async def Hbc_Student(self):
            await Hbc_StudentAvi.List().open(parent=self.locationsChildrens['bottom'])

        @SetOper(label='Время учеников', order=2, headOper="mm_student")
        async def Hbc_StudentData(self):
            await Hbc_StudentDataAvi.List().open(parent=self.locationsChildrens['bottom'])

        @SetOper(label='Выполненые практические', order=3, headOper="mm_student")
        async def Hbc_StudentLesson(self):
            await Hbc_StudentLessonAvi.List().open(parent=self.locationsChildrens['bottom'])