# Системный файл для интерфейса
from core.empty import EmptyAvi
from .Bc_TimeLineApi import Bc_TimeLineApi, Bc_TimeLineObj
from core.type.Event import SetterEvent

class Bc_TimeLineDvi(EmptyAvi):
    thisApi = Bc_TimeLineApi

    class DviDefault(EmptyAvi.Default):
        def onRefresh(self):
            return """
                SELECT t.id,
                    t.gid,
                    t.sCode,
                    t.sName
                FROM Bc_TimeLine AS t
                    
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

        def thisRop(self)->Bc_TimeLineObj:
            return super().thisRop()

        def thisApi(self)->Bc_TimeLineApi:
            return super().thisApi()

        def setsCode(self, event:SetterEvent): self.thisApi().setsCode(self.thisRop(), event.value.getValue()['value']); self.afterSetter()
        def setsName(self, event:SetterEvent): self.thisApi().setsName(self.thisRop(), event.value.getValue()['value']); self.afterSetter()
        
    class DviList(DviDefault, EmptyAvi.List): pass

    class DviCard(DviDefault, EmptyAvi.Card): 
        def onRefresh(self):
            return self.thisApi().load(self.idItem)

    class DviLookUp(EmptyAvi.LookUp):
        def onRefresh(self):
            return """
            SELECT t.id
                ,t.sHeadLine 
            FROM Bc_TimeLine AS t
            """
