# Системный файл для интерфейса
from core.sdk import EmptyAvi, SetterEvent
from .Awh_GenreApi import Awh_GenreApi, Awh_GenreObj

class Awh_GenreDvi(EmptyAvi):
    thisApi = Awh_GenreApi

    class DviDefault(EmptyAvi.Default):
        def onRefresh(self):
            return """
                SELECT t.id,
                    t.gid,
                    t.sCaption
                FROM Awh_Genre AS t
                    
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

        def thisRop(self)->Awh_GenreObj:
            return super().thisRop()

        def thisApi(self)->Awh_GenreApi:
            return super().thisApi()

        def setsCaption(self, event:SetterEvent): self.thisApi().setsCaption(self.thisRop(), event.value); self.afterSetter('sCaption')
        
    class DviList(DviDefault, EmptyAvi.List): pass

    class DviCard(DviDefault, EmptyAvi.Card): 
        def onRefresh(self):
            return self.thisApi().load(self.idItem)

    class DviLookUp(EmptyAvi.LookUp):
        def onRefresh(self):
            return """
            SELECT t.id
                ,t.sHeadLine 
            FROM Awh_Genre AS t
            """
