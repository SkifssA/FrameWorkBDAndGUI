# Системный файл для интерфейса
from engine.base import BaseAvi, Selection, Event
from .Hbc_StudentLessonApi import Hbc_StudentLessonApi, Hbc_StudentLessonObj

class Hbc_StudentLessonDvi(BaseAvi):
    thisApi = Hbc_StudentLessonApi

    class DviDefault(BaseAvi.DefaultDefault):
        def onRefresh(self):
            return """
                SELECT t.id,
                    t.gid,
                    t.idStudent,
                    t1.sHeadLine as idStudentHL,
                    t.idLesson,
                    t2.sHeadLine as idLessonHL,
                    t.bUploadFile,
                    t.bFillScore
                FROM Hbc_StudentLesson AS t
                    LEFT JOIN Hbc_Student t1 ON t1.id = t.idStudent
                    LEFT JOIN Hbc_Lesson t2 ON t2.id = t.idLesson
                """

        def onRefreshExt(self):
            return """
                with t as ( select 
                    :id as id,
                    :idStudent as idStudent,
            :idLesson as idLesson
                )
                select
                    t.id,
                  t1.sHeadLine as idStudentHL,
                    t2.sHeadLine as idLessonHL
                from t
                    LEFT JOIN Hbc_Student t1 ON t1.id = t.idStudent
            LEFT JOIN Hbc_Lesson t2 ON t2.id = t.idLesson
                """

        def thisRop(self)->Hbc_StudentLessonObj:
            return super().thisRop()

        def thisApi(self)->Hbc_StudentLessonApi:
            return super().thisApi()
        
        def setidStudent(self, event:Event.SetterEvent): self.thisApi().setidStudent(self.thisRop(), event.value); self.afterSetter()
        def setidStudentHL(self, event:Event.SetterEvent): 
            from ...object.student.Hbc_StudentAvi import Hbc_StudentAvi
            Hbc_StudentAvi().proccessById(event, self.getAttr('idStudent'), lambda x: self.thisApi().setidStudent(self.thisRop(), x['id'])); self.afterSetter()
        def setidLesson(self, event:Event.SetterEvent): self.thisApi().setidLesson(self.thisRop(), event.value); self.afterSetter()
        def setidLessonHL(self, event:Event.SetterEvent): 
            from ...object.lesson.Hbc_LessonAvi import Hbc_LessonAvi
            Hbc_LessonAvi().proccessById(event, self.getAttr('idLesson'), lambda x: self.thisApi().setidLesson(self.thisRop(), x['id'])); self.afterSetter()
        def setbUploadFile(self, event:Event.SetterEvent): self.thisApi().setbUploadFile(self.thisRop(), event.value); self.afterSetter()
        def setbFillScore(self, event:Event.SetterEvent): self.thisApi().setbFillScore(self.thisRop(), event.value); self.afterSetter()

    class DviList(DviDefault, BaseAvi.DefaultList): pass

    class DviCard(DviDefault, BaseAvi.DefaultCard): 
        def onRefresh(self):
            return self.thisApi().load(self.idItem)

    class DviLookUp(BaseAvi.DefaultLookUp):
        def onRefresh(self):
            return """
            SELECT t.id
                ,t.sHeadLine 
            FROM Hbc_StudentLesson AS t
            """
