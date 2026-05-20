# Пользовательский файл для интерфейса
from .Core_ClassDvi import Core_ClassDvi
from engine.fabric.Form import FormConstruct

class Core_ClassAvi(Core_ClassDvi):
    class List(Core_ClassDvi.DviList): pass

    class Card(Core_ClassDvi.DviCard): pass

    class LookUp(Core_ClassDvi.DviLookUp): pass

    @classmethod
    def list(cls)->FormConstruct:
        return FormConstruct(cls.List)
    
    @classmethod
    def card(cls)->FormConstruct:
        return FormConstruct(cls.Card)
