# Пользовательский файл для интерфейса
from .Gmb_TaskDvi import Gmb_TaskDvi
from engine.fabric.Form import FormConstruct

class Gmb_TaskAvi(Gmb_TaskDvi):
    class List(Gmb_TaskDvi.DviList): 
        def openCh(self):
            from modules.gmb import Gmb_ModAvi
            yield Gmb_ModAvi.list().param(locat='right')

    class Card(Gmb_TaskDvi.DviCard): pass

    class LookUp(Gmb_TaskDvi.DviLookUp): pass

    @classmethod
    def list(cls)->FormConstruct:
        return FormConstruct(cls.List)
    
    @classmethod
    def card(cls)->FormConstruct:
        return FormConstruct(cls.Card)
