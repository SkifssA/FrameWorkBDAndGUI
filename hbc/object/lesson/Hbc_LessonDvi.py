# Системный файл для интерфейса
from core.base import BaseAvi, Selection
from .Hbc_LessonApi import Hbc_LessonApi, Hbc_LessonObj

class Hbc_LessonDvi(BaseAvi):
    thisApi = Hbc_LessonApi
    class DviDefault(BaseAvi.DefaultDefault):
        async def onRefresh(self):
            return """
            SELECT t.id,
                   t.gid,
                   t.sCaption,
                   t.sIdExit
            FROM Hbc_Lesson AS t
                   
            """

        async def thisRop(self)->Hbc_LessonObj:
            return await super().thisRop()

        def thisApi(self)->Hbc_LessonApi:
            return super().thisApi()

    class DviList(DviDefault, BaseAvi.DefaultList): pass

    class DviCard(DviDefault, BaseAvi.DefaultCard): pass

    class DviLookUp(BaseAvi.DefaultLookUp):
        async def onRefresh(self):
            return """
            SELECT t.id
                  ,t.sHeadLine 
            FROM Hbc_Lesson AS t
            """
