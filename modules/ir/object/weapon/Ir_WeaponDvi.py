# Системный файл для интерфейса
from core.base import BaseAvi, Selection
from .Ir_WeaponApi import Ir_WeaponApi, Ir_WeaponObj

class Ir_WeaponDvi(BaseAvi):
    thisApi = Ir_WeaponApi
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
                FROM Ir_Weapon AS t
                    LEFT JOIN Ir_WeaponType t1 ON t1.id = t.idType
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
                    LEFT JOIN Ir_WeaponType t1 ON t1.id = t.idType
            LEFT JOIN Ir_Rare t2 ON t2.id = t.idRare
                """

        async def thisRop(self)->Ir_WeaponObj:
            return await super().thisRop()

        def thisApi(self)->Ir_WeaponApi:
            return super().thisApi()
        
        def setsCaption(self, sender, app_data, user_data): self.thisApi().setsCaption(self.obj, app_data); self.afterSetter()
        def setidType(self, sender, app_data, user_data): self.thisApi().setidType(self.obj, app_data); self.afterSetter()
        def setidRare(self, sender, app_data, user_data): self.thisApi().setidRare(self.obj, app_data); self.afterSetter()
        def setnScore(self, sender, app_data, user_data): self.thisApi().setnScore(self.obj, app_data); self.afterSetter()

    class DviList(DviDefault, BaseAvi.DefaultList): pass

    class DviCard(DviDefault, BaseAvi.DefaultCard): pass

    class DviLookUp(BaseAvi.DefaultLookUp):
        async def onRefresh(self):
            return """
            SELECT t.id
                ,t.sHeadLine 
            FROM Ir_Weapon AS t
            """
