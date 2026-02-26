# Пользовательский файл для интерфейса
from .Ir_ItemDvi import Ir_ItemDvi

class Ir_ItemAvi(Ir_ItemDvi):
    class List(Ir_ItemDvi.DviList): 
        async def onRefresh(self):
            return """
                SELECT t.id,
                    t.gid,
                    t.gidScr,
                    coalesce(t1.sHEadLine, t2.sHEadLine, t3.sHEadLine) as gidScrHL
                FROM Ir_Item AS t
                    left join Ir_ItemLoot t1 on t1.gid = t.gidScr
                    left join Ir_Weapon t2 on t2.gid = t.gidScr
                    left join Ir_Defa t3 on t3.gid = t.gidScr
                """

    class Card(Ir_ItemDvi.DviCard): pass

    class LookUp(Ir_ItemDvi.DviLookUp): pass

    @classmethod
    def list(cls, **kwargs)->List:
        return cls.typeMeta(cls.List, **kwargs)
    
    @classmethod
    def card(cls, **kwargs)->Card:
        return cls.typeMeta(cls.Card, **kwargs)
