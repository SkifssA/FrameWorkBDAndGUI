# Системный файл для интерфейса
from core.base import BaseAvi, Selection
from .Ir_HeroTypeApi import Ir_HeroTypeApi, Ir_HeroTypeObj

class Ir_HeroTypeDvi(BaseAvi):
    thisApi = Ir_HeroTypeApi
    class DviDefault(BaseAvi.DefaultDefault):
        async def onRefresh(self):
            return """
                SELECT t.id,
                    t.gid,
                    t.sCaption,
                    t.sCode,
                    t.idWeaponType,
                    t1.sHeadLine as idWeaponTypeHL,
                    t.idDefType,
                    t2.sHeadLine as idDefTypeHL
                FROM Ir_HeroType AS t
                    LEFT JOIN Ir_WeaponType t1 ON t1.id = t.idWeaponType
                    LEFT JOIN Ir_DefType t2 ON t2.id = t.idDefType
                """

        def onRefreshExt(self):
            return """
                with t as ( select 
                    :idWeaponType as idWeaponType,
            :idDefType as idDefType
                )
                select t1.sHeadLine as idWeaponTypeHL,
                    t2.sHeadLine as idDefTypeHL
                from t
                    LEFT JOIN Ir_WeaponType t1 ON t1.id = t.idWeaponType
            LEFT JOIN Ir_DefType t2 ON t2.id = t.idDefType
                """

        async def thisRop(self)->Ir_HeroTypeObj:
            return await super().thisRop()

        def thisApi(self)->Ir_HeroTypeApi:
            return super().thisApi()
        
        def setsCaption(self, sender, app_data, user_data): self.thisApi().setsCaption(self.obj, app_data); self.afterSetter()
        def setsCode(self, sender, app_data, user_data): self.thisApi().setsCode(self.obj, app_data); self.afterSetter()
        def setidWeaponType(self, sender, app_data, user_data): self.thisApi().setidWeaponType(self.obj, app_data); self.afterSetter()
        def setidDefType(self, sender, app_data, user_data): self.thisApi().setidDefType(self.obj, app_data); self.afterSetter()

    class DviList(DviDefault, BaseAvi.DefaultList): pass

    class DviCard(DviDefault, BaseAvi.DefaultCard): pass

    class DviLookUp(BaseAvi.DefaultLookUp):
        async def onRefresh(self):
            return """
            SELECT t.id
                ,t.sHeadLine 
            FROM Ir_HeroType AS t
            """
