# Системный файл для интерфейса
from engine.base import BaseAvi, Selection, Event
from .Core_AttributeApi import Core_AttributeApi, Core_AttributeObj

class Core_AttributeDvi(BaseAvi):
    thisApi = Core_AttributeApi

    class DviDefault(BaseAvi.DefaultDefault):
        def onRefresh(self):
            return """
                SELECT t.id,
                    t.gid,
                    t.sCode,
                    t.sCaption,
                    t.idClass,
                    t1.sHeadLine as idClassHL
                FROM Core_Attribute AS t
                    LEFT JOIN Core_Class t1 ON t1.id = t.idClass
                """

        def onRefreshExt(self):
            return """
                with t as ( select 
                    :id as id
                    :idClass as idClass
                )
                select
                    t.id
                  t1.sHeadLine as idClassHL
                from t
                    LEFT JOIN Core_Class t1 ON t1.id = t.idClass
                """

        def thisRop(self)->Core_AttributeObj:
            return super().thisRop()

        def thisApi(self)->Core_AttributeApi:
            return super().thisApi()
        
        def setsCode(self, event:Event.SetterEvent): self.thisApi().setsCode(self.thisRop(), event.value); self.afterSetter()
        def setsCaption(self, event:Event.SetterEvent): self.thisApi().setsCaption(self.thisRop(), event.value); self.afterSetter()
        def setidClass(self, event:Event.SetterEvent): self.thisApi().setidClass(self.thisRop(), event.value); self.afterSetter()
        def setidClassHL(self, event:Event.SetterEvent): event.user_data._getAvi()().proccessById(event, self.getAttr('idClass'), lambda x: self.thisApi().setidClass(self.thisRop(), x['id'])); self.afterSetter()

    class DviList(DviDefault, BaseAvi.DefaultList): pass

    class DviCard(DviDefault, BaseAvi.DefaultCard): pass

    class DviLookUp(BaseAvi.DefaultLookUp):
        def onRefresh(self):
            return """
            SELECT t.id
                ,t.sHeadLine 
            FROM Core_Attribute AS t
            """
