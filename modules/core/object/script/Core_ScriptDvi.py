# Системный файл для интерфейса
from engine.base import BaseAvi, Selection, Event
from .Core_ScriptApi import Core_ScriptApi, Core_ScriptObj

class Core_ScriptDvi(BaseAvi):
    thisApi = Core_ScriptApi

    class DviDefault(BaseAvi.DefaultDefault):
        def onRefresh(self):
            return """
                SELECT t.id,
                    t.gid,
                    t.sCode,
                    t.nVersion
                FROM Core_Script AS t
                    
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

        def thisRop(self)->Core_ScriptObj:
            return super().thisRop()

        def thisApi(self)->Core_ScriptApi:
            return super().thisApi()
        
        def setsCode(self, event:Event.SetterEvent): self.thisApi().setsCode(self.thisRop(), event.value); self.afterSetter()
        def setnVersion(self, event:Event.SetterEvent): self.thisApi().setnVersion(self.thisRop(), event.value); self.afterSetter()

    class DviList(DviDefault, BaseAvi.DefaultList): pass

    class DviCard(DviDefault, BaseAvi.DefaultCard): 
        def onRefresh(self):
            return self.thisApi().load(self.idItem)

    class DviLookUp(BaseAvi.DefaultLookUp):
        def onRefresh(self):
            return """
            SELECT t.id
                ,t.sHeadLine 
            FROM Core_Script AS t
            """
