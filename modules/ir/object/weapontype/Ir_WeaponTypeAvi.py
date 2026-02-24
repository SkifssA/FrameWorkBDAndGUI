# Пользовательский файл для интерфейса
from .Ir_WeaponTypeDvi import Ir_WeaponTypeDvi

class Ir_WeaponTypeAvi(Ir_WeaponTypeDvi):
    class List(Ir_WeaponTypeDvi.DviList): pass

    class Card(Ir_WeaponTypeDvi.DviCard): pass

    class LookUp(Ir_WeaponTypeDvi.DviLookUp): pass

    @classmethod
    def list(cls, **kwargs)->List:
        return cls.typeMeta(cls.List, **kwargs)
    
    @classmethod
    def card(cls, **kwargs)->Card:
        return cls.typeMeta(cls.Card, **kwargs)
