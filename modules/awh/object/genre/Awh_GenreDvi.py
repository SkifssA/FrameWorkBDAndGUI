# Системный файл для интерфейса
from engine.base import BaseAvi, Selection, Event
from .Awh_GenreApi import Awh_GenreApi, Awh_GenreObj

class Awh_GenreDvi(BaseAvi):
    thisApi = Awh_GenreApi

    class DviDefault(BaseAvi.DefaultDefault):
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
        
        def setsCaption(self, event:Event.SetterEvent): self.thisApi().setsCaption(self.thisRop(), event.value); self.afterSetter()

    class DviList(DviDefault, BaseAvi.DefaultList): pass

    class DviCard(DviDefault, BaseAvi.DefaultCard): pass

    class DviLookUp(BaseAvi.DefaultLookUp):
        def onRefresh(self):
            return """
            SELECT t.id
                ,t.sHeadLine 
            FROM Awh_Genre AS t
            """
