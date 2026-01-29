# Системный файл для интерфейса
from core.base import BaseAvi, Selection
from .Hbc_StudentApi import Hbc_StudentApi, Hbc_StudentObj

class Hbc_StudentDvi(BaseAvi):
    thisApi = Hbc_StudentApi
    class DviDefault(BaseAvi.DefaultDefault):
        async def onRefresh(self):
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

        async def thisRop(self)->Hbc_StudentObj:
            return await super().thisRop()

        def thisApi(self)->Hbc_StudentApi:
            return super().thisApi()
        
        def setsName(self, sender, app_data, user_data): self.thisApi().setsName(self.obj, app_data); self.afterSetter()
        def setsContact(self, sender, app_data, user_data): self.thisApi().setsContact(self.obj, app_data); self.afterSetter()
        def setsIpVM(self, sender, app_data, user_data): self.thisApi().setsIpVM(self.obj, app_data); self.afterSetter()
        def setsLoginVM(self, sender, app_data, user_data): self.thisApi().setsLoginVM(self.obj, app_data); self.afterSetter()
        def setsPassworVM(self, sender, app_data, user_data): self.thisApi().setsPassworVM(self.obj, app_data); self.afterSetter()
        def setsIdNew(self, sender, app_data, user_data): self.thisApi().setsIdNew(self.obj, app_data); self.afterSetter()
        def setbEnd(self, sender, app_data, user_data): self.thisApi().setbEnd(self.obj, app_data); self.afterSetter()

    class DviList(DviDefault, BaseAvi.DefaultList): pass

    class DviCard(DviDefault, BaseAvi.DefaultCard): pass

    class DviLookUp(BaseAvi.DefaultLookUp):
        async def onRefresh(self):
            return """
            SELECT t.id
                ,t.sHeadLine 
            FROM Hbc_Student AS t
            """
