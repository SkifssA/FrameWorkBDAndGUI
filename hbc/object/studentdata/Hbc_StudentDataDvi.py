# Системный файл для интерфейса
from core.base import BaseAvi, Selection
from .Hbc_StudentDataApi import Hbc_StudentDataApi, Hbc_StudentDataObj

class Hbc_StudentDataDvi(BaseAvi):
    thisApi = Hbc_StudentDataApi
    class DviList(BaseAvi.DefaultList):
        showAttr = ['idStudentHL', 'sData']
        selection = Selection('Hbc_StudentData')
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

        async def thisRop(self)->Hbc_StudentDataObj:
            return await super().thisRop()

        async def thisApi(self)->Hbc_StudentDataApi:
            return super().thisApi()

    class DviLookUp(BaseAvi.DefaultLookUp):
        async def onRefresh(self):
            return """
            SELECT t.id
                  ,t.sHeadLine 
            FROM Hbc_StudentData AS t
            """
