# Системный файл для интерфейса
from engine.base import BaseAvi, Selection, Event
from .Hbc_StudentDataApi import Hbc_StudentDataApi, Hbc_StudentDataObj

class Hbc_StudentDataDvi(BaseAvi):
    thisApi = Hbc_StudentDataApi

    class DviDefault(BaseAvi.DefaultDefault):
        def onRefresh(self):
            return """
                SELECT t.id,
                    t.gid,
                    t.idStudent,
                    t1.sHeadLine as idStudentHL,
                    t.sData
                FROM Hbc_StudentData AS t
                    LEFT JOIN Hbc_Student t1 ON t1.id = t.idStudent
                """

        def onRefreshExt(self):
            return """
                with t as ( select 
                    :id as id,
                    :idStudent as idStudent
                )
                select
                    t.id,
                  t1.sHeadLine as idStudentHL
                from t
                    LEFT JOIN Hbc_Student t1 ON t1.id = t.idStudent
                """

        def thisRop(self)->Hbc_StudentDataObj:
            return super().thisRop()

        def thisApi(self)->Hbc_StudentDataApi:
            return super().thisApi()
        
        def setidStudent(self, event:Event.SetterEvent): self.thisApi().setidStudent(self.thisRop(), event.value); self.afterSetter()
        def setidStudentHL(self, event:Event.SetterEvent): 
            from ...object.student.Hbc_StudentAvi import Hbc_StudentAvi
            Hbc_StudentAvi().proccessById(event, self.getAttr('idStudent'), lambda x: self.thisApi().setidStudent(self.thisRop(), x['id'])); self.afterSetter()
        def setsData(self, event:Event.SetterEvent): self.thisApi().setsData(self.thisRop(), event.value); self.afterSetter()

    class DviList(DviDefault, BaseAvi.DefaultList): pass

    class DviCard(DviDefault, BaseAvi.DefaultCard): 
        def onRefresh(self):
            return self.thisApi().load(self.idItem)

    class DviLookUp(BaseAvi.DefaultLookUp):
        def onRefresh(self):
            return """
            SELECT t.id
                ,t.sHeadLine 
            FROM Hbc_StudentData AS t
            """
