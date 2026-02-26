# Пользовательский файл для интерфейса
import random

from .Ir_HeroDvi import Ir_HeroDvi
from core.base.BaseOper import SetOper

from modules.bc.object.log.Bc_LogApi import Bc_LogApi
from modules.bc.object.log.Bc_LogAvi import Bc_LogAvi
from modules.ir.object.weapon.Ir_WeaponApi import Ir_WeaponApi
from modules.ir.object.defa.Ir_DefaApi import Ir_DefaApi
from modules.ir.object.Itemloot.Ir_ItemLootApi import Ir_ItemLootApi
from modules.ir.object.Item.Ir_ItemApi import Ir_ItemApi

class Ir_HeroAvi(Ir_HeroDvi):
    class List(Ir_HeroDvi.DviList): pass

    class Card(Ir_HeroDvi.DviCard): 
        @SetOper(label='Рейд', img='8')
        async def raidOne(self):
            loot = (Ir_WeaponApi, Ir_DefaApi, Ir_ItemLootApi)
            t = ''
            if (random.randint(0, 1)):
                t += 'Победа'
                if True:
                    cl = random.choice(loot)
                    w = await cl().getRandomId()
                    await Ir_ItemApi().insertByItem(w['gid'])
                    sCaptionW = cl().calcHeadLine(await cl().load(w['id']))
                    t+= f' Предмет: {sCaptionW}'
            else:
                t += 'Проигрыш'
            await Bc_LogApi().insertByMess(t)
            await self.selection.findSelection(Bc_LogAvi.list()).refresh()

    class LookUp(Ir_HeroDvi.DviLookUp): pass

    @classmethod
    def list(cls, **kwargs)->List:
        return cls.typeMeta(cls.List, **kwargs)
    
    @classmethod
    def card(cls, **kwargs)->Card:
        return cls.typeMeta(cls.Card, **kwargs)
