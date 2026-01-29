# Системный файл для интерфейса
from core.base import BaseAvi, Selection
from .Hbc_StudentDataApi import Hbc_StudentDataApi, Hbc_StudentDataObj

class Hbc_StudentDataDvi(BaseAvi):
    thisApi = Hbc_StudentDataApi
    class DviDefault(BaseAvi.DefaultDefault):
        async def onRefresh(self):
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
                    :idStudent as idStudent
                )
                select t1.sHeadLine as idStudentHL
                from t
                    LEFT JOIN Hbc_Student t1 ON t1.id = t.idStudent
                """

        async def thisRop(self)->Hbc_StudentDataObj:
            return await super().thisRop()

        def thisApi(self)->Hbc_StudentDataApi:
            return super().thisApi()
        
        def setidStudent(self, sender, app_data, user_data): self.thisApi().setidStudent(self.obj, app_data); self.afterSetter()
        def setsData(self, sender, app_data, user_data): self.thisApi().setsData(self.obj, app_data); self.afterSetter()

    class DviList(DviDefault, BaseAvi.DefaultList): pass

    class DviCard(DviDefault, BaseAvi.DefaultCard): pass

    class DviLookUp(BaseAvi.DefaultLookUp):
        async def onRefresh(self):
            return """
            SELECT t.id
                ,t.sHeadLine 
            FROM Hbc_StudentData AS t
            """
