# Системный файл для интерфейса
from .Sc_ScriptsLogic import Sc_ScriptsLogic, Sc_ScriptsObj
from core.sdk import EmptyPub, SetterEvent, Setter

class Sc_ScriptsDvi(EmptyPub):
    thisLogic = Sc_ScriptsLogic

    class DviDefault(EmptyPub.Default):
        def structuredQuery(self):
            return """
                SELECT t.id,
                    t.sCode,
                    t.idCls,
                    t1.sHeadLine as idClsHL,
                    t.nVer
                FROM Sc_Scripts AS t
                    LEFT JOIN Sc_Cls t1 ON t1.id = t.idCls
                """

        def onRefreshExt(self):
            return """
                with t as ( select 
                    :id as id,
                    :idCls as idCls
                )
                select
                    t.id,
                  t1.sHeadLine as idClsHL
                from t
                    LEFT JOIN Sc_Cls t1 ON t1.id = t.idCls
                """

        def thisLogic(self)->Sc_ScriptsLogic:
            return super().thisLogic()

        @Setter
        def setsCode(self, event:SetterEvent): self.thisLogic().setsCode(self.thisObj(), event.value); self.afterSetter('sCode')
        @Setter
        def setidCls(self, event:SetterEvent): self.thisLogic().setidCls(self.thisObj(), event.value); self.afterSetter('idCls')
        @Setter
        def setidClsHL(self, event:SetterEvent): self.thisLogic().setidClsHL(self.thisObj(), event.value); self.afterSetter('idClsHL')
        @Setter
        def setnVer(self, event:SetterEvent): self.thisLogic().setnVer(self.thisObj(), event.value); self.afterSetter('nVer')
        
    class DviList(DviDefault, EmptyPub.List):...

    class DviCard(DviDefault, EmptyPub.Card):...

    class DviLookUp:
        def onRefresh(self):
            return """
            SELECT t.id
                ,t.sHeadLine 
            FROM Sc_Scripts AS t
            """
