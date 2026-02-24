# Пользовательский файл для интерфейса
from .Ir_WeaponDvi import Ir_WeaponDvi

class Ir_WeaponAvi(Ir_WeaponDvi):
    class List(Ir_WeaponDvi.DviList): pass

    class Card(Ir_WeaponDvi.DviCard): pass

    class LookUp(Ir_WeaponDvi.DviLookUp): pass

    @classmethod
    def list(cls, **kwargs)->List:
        return cls.typeMeta(cls.List, **kwargs)
    
    @classmethod
    def card(cls, **kwargs)->Card:
        return cls.typeMeta(cls.Card, **kwargs)
