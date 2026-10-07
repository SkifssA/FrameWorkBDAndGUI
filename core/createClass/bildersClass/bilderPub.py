from .bilderBase import BilderBase

class BilderPub(BilderBase):
    temp = """# Пользовательский файл для интерфейса
from .{name}Dvi import {name}Dvi

class {name}Pub({name}Dvi):
    class List({name}Dvi.DviList): pass

    class Card({name}Dvi.DviCard): pass

    class LookUp({name}Dvi.DviLookUp): pass
"""
    suffixFile = 'Pub.py'
