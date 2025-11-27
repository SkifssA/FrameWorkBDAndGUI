# Системный файл для интерфейса
from core.base import BaseAvi, Selection
from .Hbc_StudentApi import Hbc_StudentApi, Hbc_StudentObj

class Hbc_StudentDvi(BaseAvi):
    thisApi = Hbc_StudentApi
    class DviDefault(BaseAvi.DefaultDefault):
        selection = lambda self: Selection(self.getTag())
        async def onRefresh(self):
            return """
            SELECT t.id,
                   t.gid,
                   t.sName,
                   t.sContact,
                   t.sIpVM,
                   t.sLoginVM,
                   t.sPassworVM,
                   t.sIdNew,
                   t.bEnd
            FROM Hbc_Student AS t
                   
            """

        async def thisRop(self)->Hbc_StudentObj:
            return await super().thisRop()

        def thisApi(self)->Hbc_StudentApi:
            return super().thisApi()

    class DviList(DviDefault, BaseAvi.DefaultList): pass

    class DviLookUp(BaseAvi.DefaultLookUp):
        async def onRefresh(self):
            return """
            SELECT t.id
                  ,t.sHeadLine 
            FROM Hbc_Student AS t
            """
