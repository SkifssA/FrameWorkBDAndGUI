from .bilderBase import BilderBase

class BilderAvi(BilderBase):
    temp = """# Пользовательский файл для интерфейса
from .{name}Dvi import {name}Dvi

class {name}Avi({name}Dvi):
    class List({name}Dvi.DviList): pass

    class Card({name}Dvi.DviCard): pass

    class LookUp({name}Dvi.DviLookUp): pass
"""
    suffixFile = 'Avi.py'
