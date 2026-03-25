from .lesson.Hbc_LessonAvi import Hbc_LessonAvi
from .student.Hbc_StudentAvi import Hbc_StudentAvi
from .studentdata.Hbc_StudentDataAvi import Hbc_StudentDataAvi
from .studentlesson.Hbc_StudentLessonAvi import Hbc_StudentLessonAvi
from core.base.oper import SetOper
from core.form.MainMenu import mainMenu
from modules.bc.object.file.Bc_FileAvi import Bc_FileAvi

class Hbc_MainMenu(mainMenu):
    class Default(mainMenu.Default):
        @SetOper(label="Справочники")
        def mm_respo(self): pass

        @SetOper(label='Уроки', order=1, headOper='mm_respo')
        def Hbc_Lesson(self):
            Hbc_LessonAvi.list().param(parent=self).open()

        @SetOper(label='Файлы', order=2, headOper='mm_respo')
        def Bc_File(self):
            Bc_FileAvi.list().param(parent=self).open()

        @SetOper(label="Ученики")
        def mm_student(self):pass

        @SetOper(label='Ученики', order=1, headOper="mm_student")
        def Hbc_Student(self):
            Hbc_StudentAvi.list().param(parent=self).open()

        @SetOper(label='Время учеников', order=2, headOper="mm_student")
        def Hbc_StudentData(self):
            Hbc_StudentDataAvi.list().param(parent=self).open()

        @SetOper(label='Выполненые практические', order=3, headOper="mm_student")
        def Hbc_StudentLesson(self):
            Hbc_StudentLessonAvi.list().param(parent=self).open()