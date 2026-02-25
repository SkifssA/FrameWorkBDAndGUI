# Системный файл для интерфейса
from core.base import BaseAvi, Selection, Event
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

        def thisRop(self)->Ir_HeroObj:
            return super().thisRop()

        def thisApi(self)->Ir_HeroApi:
            return super().thisApi()
        
        def setsCaption(self, event:Event.SetterEvent): self.thisApi().setsCaption(self.thisRop(), event.value); self.afterSetter()
        def setnHead(self, event:Event.SetterEvent): self.thisApi().setnHead(self.thisRop(), event.value); self.afterSetter()
        def setnHeadMax(self, event:Event.SetterEvent): self.thisApi().setnHeadMax(self.thisRop(), event.value); self.afterSetter()
        def setnStrong(self, event:Event.SetterEvent): self.thisApi().setnStrong(self.thisRop(), event.value); self.afterSetter()
        def setnMind(self, event:Event.SetterEvent): self.thisApi().setnMind(self.thisRop(), event.value); self.afterSetter()
        def setnDexterit(self, event:Event.SetterEvent): self.thisApi().setnDexterit(self.thisRop(), event.value); self.afterSetter()
        def setidType(self, event:Event.SetterEvent): self.thisApi().setidType(self.thisRop(), event.value); self.afterSetter()
        def setidTypeHL(self, event:Event.SetterEvent): idLook = event.user_data.getId(event.value); self.thisApi().setidType(self.thisRop(), idLook); self.afterSetter()

    class DviList(DviDefault, BaseAvi.DefaultList): pass

    class DviCard(DviDefault, BaseAvi.DefaultCard): pass

    class DviLookUp(BaseAvi.DefaultLookUp):
        async def onRefresh(self):
            return """
            SELECT t.id
                ,t.sHeadLine 
            FROM Ir_Hero AS t
            """
