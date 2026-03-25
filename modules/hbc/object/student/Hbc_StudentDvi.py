# Системный файл для интерфейса
from core.base import BaseAvi, Selection, Event
from .Hbc_StudentApi import Hbc_StudentApi, Hbc_StudentObj

class Hbc_StudentDvi(BaseAvi):
    thisApi = Hbc_StudentApi

    class DviDefault(BaseAvi.DefaultDefault):
        def onRefresh(self):
            return """
                SELECT t.id,
                    t.gid,
                    t.sName,
                    t.sContact,
                    t.sIpVM,
                    t.sLoginVM,
                    t.sPassworVM,
                    t.sIdNew,
                    t.bEnd
                FROM Hbc_Student AS t
                    
                """

        def onRefreshExt(self):
            return """
                with t as ( select 
                    
                )
                select 
                from t
                    
                """

        def thisRop(self)->Hbc_StudentObj:
            return super().thisRop()

        def thisApi(self)->Hbc_StudentApi:
            return super().thisApi()
        
        def setsName(self, event:Event.SetterEvent): self.thisApi().setsName(self.thisRop(), event.value); self.afterSetter()
        def setsContact(self, event:Event.SetterEvent): self.thisApi().setsContact(self.thisRop(), event.value); self.afterSetter()
        def setsIpVM(self, event:Event.SetterEvent): self.thisApi().setsIpVM(self.thisRop(), event.value); self.afterSetter()
        def setsLoginVM(self, event:Event.SetterEvent): self.thisApi().setsLoginVM(self.thisRop(), event.value); self.afterSetter()
        def setsPassworVM(self, event:Event.SetterEvent): self.thisApi().setsPassworVM(self.thisRop(), event.value); self.afterSetter()
        def setsIdNew(self, event:Event.SetterEvent): self.thisApi().setsIdNew(self.thisRop(), event.value); self.afterSetter()
        def setbEnd(self, event:Event.SetterEvent): self.thisApi().setbEnd(self.thisRop(), event.value); self.afterSetter()

    class DviList(DviDefault, BaseAvi.DefaultList): pass

    class DviCard(DviDefault, BaseAvi.DefaultCard): pass

    class DviLookUp(BaseAvi.DefaultLookUp):
        def onRefresh(self):
            return """
            SELECT t.id
                ,t.sHeadLine 
            FROM Hbc_Student AS t
            """
