# Пользовательский файл для интерфейса
from .Gmb_ModDvi import Gmb_ModDvi
from engine.fabric.Form import FormConstruct

class Gmb_ModAvi(Gmb_ModDvi):
    class List(Gmb_ModDvi.DviList): pass

    class Card(Gmb_ModDvi.DviCard): pass

    class LookUp(Gmb_ModDvi.DviLookUp): pass

    @classmethod
    def list(cls)->FormConstruct:
        return FormConstruct(cls.List)
    
    @classmethod
    def card(cls)->FormConstruct:
        return FormConstruct(cls.Card)
