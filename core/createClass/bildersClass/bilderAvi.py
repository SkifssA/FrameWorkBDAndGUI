from .bilderBase import BilderBase

class BilderAvi(BilderBase):
    temp = """# Пользовательский файл для интерфейса
from .{nameClass}Dvi import {nameClass}Dvi
from core.sdk import FormConstruct

class {nameClass}Avi({nameClass}Dvi):
    class List({nameClass}Dvi.DviList): pass

    class Card({nameClass}Dvi.DviCard): pass

    class LookUp({nameClass}Dvi.DviLookUp): pass

    @classmethod
    def list(cls)->FormConstruct:
        return FormConstruct(cls.List)
    
    @classmethod
    def card(cls)->FormConstruct:
        return FormConstruct(cls.Card)
"""
    suffixFile = 'Avi.py'
