# Системный файл для интерфейса
from core.base import BaseAvi, Selection
from .Hbc_StudentLessonApi import Hbc_StudentLessonApi, Hbc_StudentLessonObj

class Hbc_StudentLessonDvi(BaseAvi):
    thisApi = Hbc_StudentLessonApi
    class DviDefault(BaseAvi.DefaultDefault):
        async def onRefresh(self):
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

        async def thisRop(self)->Hbc_StudentLessonObj:
            return await super().thisRop()

        def thisApi(self)->Hbc_StudentLessonApi:
            return super().thisApi()

    class DviList(DviDefault, BaseAvi.DefaultList): pass

    class DviCard(DviDefault, BaseAvi.DefaultCard): pass

    class DviLookUp(BaseAvi.DefaultLookUp):
        async def onRefresh(self):
            return """
            SELECT t.id
                  ,t.sHeadLine 
            FROM Hbc_StudentLesson AS t
            """
