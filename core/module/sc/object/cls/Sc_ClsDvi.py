# Системный файл для интерфейса
from .Sc_ClsLogic import Sc_ClsLogic, Sc_ClsObj
from core.sdk import EmptyPub, SetterEvent, Setter

class Sc_ClsDvi(EmptyPub):
    thisLogic = Sc_ClsLogic

    class DviDefault(EmptyPub.Default):
        def structuredQuery(self):
            return """
                SELECT t.id,
                    t.sCode,
                    t.sName,
                    t.nID
                FROM Sc_Cls AS t
                    
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

        def thisLogic(self)->Sc_ClsLogic:
            return super().thisLogic()

        @Setter
        def setsCode(self, event:SetterEvent): self.thisLogic().setsCode(self.thisObj(), event.value); self.afterSetter('sCode')
        @Setter
        def setsName(self, event:SetterEvent): self.thisLogic().setsName(self.thisObj(), event.value); self.afterSetter('sName')
        @Setter
        def setnID(self, event:SetterEvent): self.thisLogic().setnID(self.thisObj(), event.value); self.afterSetter('nID')
        
    class DviList(DviDefault, EmptyPub.List):...

    class DviCard(DviDefault, EmptyPub.Card):...

    class DviLookUp:
        def onRefresh(self):
            return """
            SELECT t.id
                ,t.sHeadLine 
            FROM Sc_Cls AS t
            """
