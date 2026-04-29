# Пользовательский файл для интерфейса
from .Core_AttributeDvi import Core_AttributeDvi
from engine.fabric.Form import FormConstruct

class Core_AttributeAvi(Core_AttributeDvi):
    class List(Core_AttributeDvi.DviList): pass

    class Card(Core_AttributeDvi.DviCard): pass

    class LookUp(Core_AttributeDvi.DviLookUp): pass

    @classmethod
    def list(cls)->FormConstruct:
        return FormConstruct(cls.List)
    
    @classmethod
    def card(cls)->FormConstruct:
        return FormConstruct(cls.Card)
