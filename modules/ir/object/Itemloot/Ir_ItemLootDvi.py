# Системный файл для интерфейса
from core.base import BaseAvi, Selection
from .Ir_ItemLootApi import Ir_ItemLootApi, Ir_ItemLootObj

class Ir_ItemLootDvi(BaseAvi):
    thisApi = Ir_ItemLootApi
    class DviDefault(BaseAvi.DefaultDefault):
        async def onRefresh(self):
            return """
                SELECT t.id,
                    t.gid,
                    t.sCaption,
                    t.idRare,
                    t1.sHeadLine as idRareHL,
                    t.nScore
                FROM Ir_ItemLoot AS t
                    LEFT JOIN Ir_Rare t1 ON t1.id = t.idRare
                """

        def onRefreshExt(self):
            return """
                with t as ( select 
                    :idRare as idRare
                )
                select t1.sHeadLine as idRareHL
                from t
                    LEFT JOIN Ir_Rare t1 ON t1.id = t.idRare
                """

        async def thisRop(self)->Ir_ItemLootObj:
            return await super().thisRop()

        def thisApi(self)->Ir_ItemLootApi:
            return super().thisApi()
        
        def setsCaption(self, sender, app_data, user_data): self.thisApi().setsCaption(self.obj, app_data); self.afterSetter()
        def setidRare(self, sender, app_data, user_data): self.thisApi().setidRare(self.obj, app_data); self.afterSetter()
        def setnScore(self, sender, app_data, user_data): self.thisApi().setnScore(self.obj, app_data); self.afterSetter()

    class DviList(DviDefault, BaseAvi.DefaultList): pass

    class DviCard(DviDefault, BaseAvi.DefaultCard): pass

    class DviLookUp(BaseAvi.DefaultLookUp):
        async def onRefresh(self):
            return """
            SELECT t.id
                ,t.sHeadLine 
            FROM Ir_ItemLoot AS t
            """
