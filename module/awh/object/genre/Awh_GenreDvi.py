# Системный файл для интерфейса
from .Awh_GenreLogic import Awh_GenreLogic, Awh_GenreObj
from core.sdk import EmptyPub, SetterEvent, Setter

class Awh_GenreDvi(EmptyPub):
    thisLogic = Awh_GenreLogic

    class DviDefault(EmptyPub.Default):
        def structuredQuery(self):
            return """
                SELECT t.id,
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

        def thisLogic(self)->Awh_GenreLogic:
            return super().thisLogic()

        @Setter
        def setsCaption(self, event:SetterEvent): self.thisLogic().setsCaption(self.thisObj(), event.value); self.afterSetter('sCaption')
        
    class DviList(DviDefault, EmptyPub.List):...

    class DviCard(DviDefault, EmptyPub.Card):...

    class DviLookUp:
        def onRefresh(self):
            return """
            SELECT t.id
                ,t.sHeadLine 
            FROM Awh_Genre AS t
            """
