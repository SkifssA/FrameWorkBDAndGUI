# Системный файл для интерфейса
from core.base import BaseAvi, Selection
from .Ir_HeroApi import Ir_HeroApi, Ir_HeroObj

class Ir_HeroDvi(BaseAvi):
    thisApi = Ir_HeroApi
    class DviDefault(BaseAvi.DefaultDefault):
        async def onRefresh(self):
            return """
                SELECT t.id,
                    t.gid,
                    t.sCaption,
                    t.nHead,
                    t.nHeadMax,
                    t.nStrong,
                    t.nMind,
                    t.nDexterit,
                    t.idType,
                    t1.sHeadLine as idTypeHL
                FROM Ir_Hero AS t
                    LEFT JOIN Ir_HeroType t1 ON t1.id = t.idType
                """

        def onRefreshExt(self):
            return """
                with t as ( select 
                    :idType as idType
                )
                select t1.sHeadLine as idTypeHL
                from t
                    LEFT JOIN Ir_HeroType t1 ON t1.id = t.idType
                """

        async def thisRop(self)->Ir_HeroObj:
            return await super().thisRop()

        def thisApi(self)->Ir_HeroApi:
            return super().thisApi()
        
        def setsCaption(self, sender, app_data, user_data): self.thisApi().setsCaption(self.obj, app_data); self.afterSetter()
        def setnHead(self, sender, app_data, user_data): self.thisApi().setnHead(self.obj, app_data); self.afterSetter()
        def setnHeadMax(self, sender, app_data, user_data): self.thisApi().setnHeadMax(self.obj, app_data); self.afterSetter()
        def setnStrong(self, sender, app_data, user_data): self.thisApi().setnStrong(self.obj, app_data); self.afterSetter()
        def setnMind(self, sender, app_data, user_data): self.thisApi().setnMind(self.obj, app_data); self.afterSetter()
        def setnDexterit(self, sender, app_data, user_data): self.thisApi().setnDexterit(self.obj, app_data); self.afterSetter()
        def setidType(self, sender, app_data, user_data): self.thisApi().setidType(self.obj, app_data); self.afterSetter()

    class DviList(DviDefault, BaseAvi.DefaultList): pass

    class DviCard(DviDefault, BaseAvi.DefaultCard): pass

    class DviLookUp(BaseAvi.DefaultLookUp):
        async def onRefresh(self):
            return """
            SELECT t.id
                ,t.sHeadLine 
            FROM Ir_Hero AS t
            """
