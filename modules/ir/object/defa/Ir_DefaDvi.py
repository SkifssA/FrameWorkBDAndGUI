# Системный файл для интерфейса
from core.base import BaseAvi, Selection, Event
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

        def thisRop(self)->Ir_DefaObj:
            return super().thisRop()

        def thisApi(self)->Ir_DefaApi:
            return super().thisApi()
        
        def setsCaption(self, event:Event.SetterEvent): self.thisApi().setsCaption(self.thisRop(), event.value); self.afterSetter()
        def setidType(self, event:Event.SetterEvent): self.thisApi().setidType(self.thisRop(), event.value); self.afterSetter()
        def setidTypeHL(self, event:Event.SetterEvent): idLook = event.user_data.getId(event.value); self.thisApi().setidType(self.thisRop(), idLook); self.afterSetter()
        def setidRare(self, event:Event.SetterEvent): self.thisApi().setidRare(self.thisRop(), event.value); self.afterSetter()
        def setidRareHL(self, event:Event.SetterEvent): idLook = event.user_data.getId(event.value); self.thisApi().setidRare(self.thisRop(), idLook); self.afterSetter()
        def setnScore(self, event:Event.SetterEvent): self.thisApi().setnScore(self.thisRop(), event.value); self.afterSetter()

    class DviList(DviDefault, BaseAvi.DefaultList): pass

    class DviCard(DviDefault, BaseAvi.DefaultCard): pass

    class DviLookUp(BaseAvi.DefaultLookUp):
        async def onRefresh(self):
            return """
            SELECT t.id
                ,t.sHeadLine 
            FROM Ir_Defa AS t
            """
