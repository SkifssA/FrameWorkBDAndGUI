# Системный файл для интерфейса
from core.base import BaseAvi, Selection, Event
from .Ir_ItemLootApi import Ir_ItemLootApi, Ir_ItemLootObj

from ..rare.Ir_RareAvi import Ir_RareAvi

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

        def thisRop(self)->Ir_ItemLootObj:
            return super().thisRop()

        def thisApi(self)->Ir_ItemLootApi:
            return super().thisApi()
        
        def setsCaption(self, event:Event.SetterEvent): self.thisApi().setsCaption(self.obj, event.value); self.afterSetter()
        def setidRare(self, event:Event.SetterEvent): self.thisApi().setidRare(self.obj, event.value); self.afterSetter()
        def setidRareHL(self, event:Event.SetterEvent):
            if (event.type == 'selectValue'):
                Ir_RareAvi.list().openModal(
                    callback=lambda x: self.thisApi().setidRare(self.thisRop(), x['id'])
                    )
            elif (event.type == 'openCard'):
                Ir_RareAvi.card(idItem=self.getAttr("idRare")).openModal()
            elif (event.type == 'deleteValue'):
                self.thisApi().setidRare(self.thisRop(), None)
            else:
                print("Сеттер на ввод значения")
            self.afterSetter()

        def setnScore(self, event:Event.SetterEvent): self.thisApi().setnScore(self.obj, event.value); self.afterSetter()

    class DviList(DviDefault, BaseAvi.DefaultList): pass

    class DviCard(DviDefault, BaseAvi.DefaultCard): pass

    class DviLookUp(BaseAvi.DefaultLookUp):
        async def onRefresh(self):
            return """
            SELECT t.id
                ,t.sHeadLine 
            FROM Ir_ItemLoot AS t
            """
