# Системный файл для интерфейса
from core.base import BaseAvi, Selection, Event
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

        def thisRop(self)->Ir_HeroTypeObj:
            return super().thisRop()

        def thisApi(self)->Ir_HeroTypeApi:
            return super().thisApi()
        
        def setsCaption(self, event:Event.SetterEvent): self.thisApi().setsCaption(self.thisRop(), event.value); self.afterSetter()
        def setsCode(self, event:Event.SetterEvent): self.thisApi().setsCode(self.thisRop(), event.value); self.afterSetter()
        def setidWeaponType(self, event:Event.SetterEvent): self.thisApi().setidWeaponType(self.thisRop(), event.value); self.afterSetter()
        def setidWeaponTypeHL(self, event:Event.SetterEvent): event.user_data._getAvi()().proccessById(event, self.getAttr('idWeaponType'), lambda x: self.thisApi().setidRare(self.thisRop(), x['id'])); self.afterSetter()
        def setidDefType(self, event:Event.SetterEvent): self.thisApi().setidDefType(self.thisRop(), event.value); self.afterSetter()
        def setidDefTypeHL(self, event:Event.SetterEvent): event.user_data._getAvi()().proccessById(event, self.getAttr('idDefType'), lambda x: self.thisApi().setidRare(self.thisRop(), x['id'])); self.afterSetter()

    class DviList(DviDefault, BaseAvi.DefaultList): pass

    class DviCard(DviDefault, BaseAvi.DefaultCard): pass

    class DviLookUp(BaseAvi.DefaultLookUp):
        async def onRefresh(self):
            return """
            SELECT t.id
                ,t.sHeadLine 
            FROM Ir_HeroType AS t
            """
