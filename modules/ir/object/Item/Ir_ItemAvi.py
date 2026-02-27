# Пользовательский файл для интерфейса
from .Ir_ItemDvi import Ir_ItemDvi

from ..defa.Ir_DefaApi import Ir_DefaApi
from ..weapon.Ir_WeaponApi import Ir_WeaponApi

class Ir_ItemAvi(Ir_ItemDvi):
    class List(Ir_ItemDvi.DviList): 
        async def onRefresh(self):
            return """
                SELECT t.id
                    ,t.gid
                    ,t.gidScr
                    ,coalesce(t1.sHeadLine, t2.sHeadLine, t3.sHeadLine) as gidScrHL
                    ,t4.sHeadLine as idRareHL
                    ,t5.sHeadLine as idHeroHL
                FROM Ir_Item AS t
                    left join Ir_ItemLoot t1 on t1.gid = t.gidScr
                    left join Ir_Weapon t2 on t2.gid = t.gidScr
                    left join Ir_Defa t3 on t3.gid = t.gidScr
                    left join Ir_Rare t4 on coalesce(t1.idRare, t2.idRare, t3.idRare) = t4.id
                    left join Ir_Hero t5 on t.id = t5.idDefa or t.id = t5.idWeapon
                """

    class List_Defa(List):
        async def onRefresh(self):
            return f"""
                SELECT t.id
                    ,t.gid
                    ,t.gidScr
                    ,coalesce(t1.sHeadLine, t2.sHeadLine, t3.sHeadLine) as gidScrHL
                    ,t4.sHeadLine as idRareHL
                FROM Ir_Item AS t
                    left join Ir_ItemLoot t1 on t1.gid = t.gidScr
                    left join Ir_Weapon t2 on t2.gid = t.gidScr
                    left join Ir_Defa t3 on t3.gid = t.gidScr
                    left join Ir_Rare t4 on coalesce(t1.idRare, t2.idRare, t3.idRare) = t4.id
                where SUBSTR(t.gidScr, 1, INSTR(t.gidScr, '/') - 1) = '{await Ir_DefaApi().idClass()}'
                """
        
    class List_Weapon(List):
        async def onRefresh(self):
            return f"""
                SELECT t.id
                    ,t.gid
                    ,t.gidScr
                    ,coalesce(t1.sHeadLine, t2.sHeadLine, t3.sHeadLine) as gidScrHL
                    ,t4.sHeadLine as idRareHL
                FROM Ir_Item AS t
                    left join Ir_ItemLoot t1 on t1.gid = t.gidScr
                    left join Ir_Weapon t2 on t2.gid = t.gidScr
                    left join Ir_Defa t3 on t3.gid = t.gidScr
                    left join Ir_Rare t4 on coalesce(t1.idRare, t2.idRare, t3.idRare) = t4.id
                where SUBSTR(t.gidScr, 1, INSTR(t.gidScr, '/') - 1) = '{await Ir_WeaponApi().idClass()}'
                """

    class Card(Ir_ItemDvi.DviCard): pass

    class LookUp(Ir_ItemDvi.DviLookUp): pass

    @classmethod
    def list(cls, **kwargs)->List:
        return cls.typeMeta(cls.List, **kwargs)
    
    @classmethod
    def list_Defa(cls, **kwargs)->List_Defa:
        return cls.typeMeta(cls.List_Defa, **kwargs)
    
    @classmethod
    def list_Weapon(cls, **kwargs)->List_Weapon:
        return cls.typeMeta(cls.List_Weapon, **kwargs)
    
    @classmethod
    def card(cls, **kwargs)->Card:
        return cls.typeMeta(cls.Card, **kwargs)
