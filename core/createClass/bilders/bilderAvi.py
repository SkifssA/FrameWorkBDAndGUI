from .bilderBase import BilderBase

class BilderAvi(BilderBase):
    temp = """# Пользовательский файл для интерфейса
from .{nameClass}Dvi import {nameClass}Dvi

class {nameClass}Avi({nameClass}Dvi):
    class List({nameClass}Dvi.DviList): pass

    class Card({nameClass}Dvi.DviCard): pass

    class LookUp({nameClass}Dvi.DviLookUp): pass

    @classmethod
    def list(cls, **kwargs)->List:
        return cls.typeMeta(cls.List, **kwargs)
    
    @classmethod
    def card(cls, **kwargs)->Card:
        return cls.typeMeta(cls.Card, **kwargs)
"""
    suffixFile = 'Avi.py'
