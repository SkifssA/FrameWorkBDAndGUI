# Системный файл для интерфейса
from engine.base import BaseAvi, Selection, Event
from .Core_ClassApi import Core_ClassApi, Core_ClassObj

class Core_ClassDvi(BaseAvi):
    thisApi = Core_ClassApi

    class DviDefault(BaseAvi.DefaultDefault):
        def onRefresh(self):
            return """
                SELECT t.id,
                    t.gid,
                    t.sCode,
                    t.sCaption
                FROM Core_Class AS t
                    
                """

        def onRefreshExt(self):
            return """
                with t as ( select 
                    :id as id
                    
                )
                select
                    t.id
                  
                from t
                    
                """

        def thisRop(self)->Core_ClassObj:
            return super().thisRop()

        def thisApi(self)->Core_ClassApi:
            return super().thisApi()
        
        def setsCode(self, event:Event.SetterEvent): self.thisApi().setsCode(self.thisRop(), event.value); self.afterSetter()
        def setsCaption(self, event:Event.SetterEvent): self.thisApi().setsCaption(self.thisRop(), event.value); self.afterSetter()

    class DviList(DviDefault, BaseAvi.DefaultList): pass

    class DviCard(DviDefault, BaseAvi.DefaultCard): 
        def onRefresh(self):
            return self.thisApi().load(self.idItem)

    class DviLookUp(BaseAvi.DefaultLookUp):
        def onRefresh(self):
            return """
            SELECT t.id
                ,t.sHeadLine 
            FROM Core_Class AS t
            """
