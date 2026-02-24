# Системный файл для интерфейса
from core.base import BaseAvi, Selection
from .Ir_DefaApi import Ir_DefaApi, Ir_DefaObj

class Ir_DefaDvi(BaseAvi):
    thisApi = Ir_DefaApi
    class DviDefault(BaseAvi.DefaultDefault):
        async def onRefresh(self):
            return """
                SELECT t.id,
                    t.gid,
                    t.sCaption,
                    t.idType,
                    t1.sHeadLine as idTypeHL,
                    t.idRare,
                    t2.sHeadLine as idRareHL,
                    t.nScore
                FROM Ir_Defa AS t
                    LEFT JOIN Ir_DefType t1 ON t1.id = t.idType
                    LEFT JOIN Ir_Rare t2 ON t2.id = t.idRare
                """

        def onRefreshExt(self):
            return """
                with t as ( select 
                    :idType as idType,
            :idRare as idRare
                )
                select t1.sHeadLine as idTypeHL,
                    t2.sHeadLine as idRareHL
                from t
                    LEFT JOIN Ir_DefType t1 ON t1.id = t.idType
            LEFT JOIN Ir_Rare t2 ON t2.id = t.idRare
                """

        async def thisRop(self)->Ir_DefaObj:
            return await super().thisRop()

        def thisApi(self)->Ir_DefaApi:
            return super().thisApi()
        
        def setsCaption(self, sender, app_data, user_data): self.thisApi().setsCaption(self.obj, app_data); self.afterSetter()
        def setidType(self, sender, app_data, user_data): self.thisApi().setidType(self.obj, app_data); self.afterSetter()
        def setidTypeHL(self, sender, app_data, user_data): idLook = user_data.getId(app_data); self.thisApi().setidType(self.obj, idLook); self.afterSetter()
        def setidRare(self, sender, app_data, user_data): self.thisApi().setidRare(self.obj, app_data); self.afterSetter()
        def setidRareHL(self, sender, app_data, user_data): idLook = user_data.getId(app_data); self.thisApi().setidRare(self.obj, idLook); self.afterSetter()
        def setnScore(self, sender, app_data, user_data): self.thisApi().setnScore(self.obj, app_data); self.afterSetter()

    class DviList(DviDefault, BaseAvi.DefaultList): pass

    class DviCard(DviDefault, BaseAvi.DefaultCard): pass

    class DviLookUp(BaseAvi.DefaultLookUp):
        async def onRefresh(self):
            return """
            SELECT t.id
                ,t.sHeadLine 
            FROM Ir_Defa AS t
            """
