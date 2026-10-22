from .builderBase import builderBase


class builderPub(builderBase):
    temp = """# Пользовательский файл для интерфейса
from .{name}Dvi import {name}Dvi
from core.sdk import Form

class {name}Pub({name}Dvi):

    metaFile = \'{name}.Ameta.json\'

    class List({name}Dvi.DviList): pass

    class Card({name}Dvi.DviCard): pass

    class LookUp({name}Dvi.DviLookUp): pass

    @classmethod
    def list(cls, **kwargs): return Form(cls.List, cls, **kwargs)

    @classmethod
    def card(cls, **kwargs): return Form(cls.Card, cls, **kwargs)
"""
    suffixFile = "Pub.py"
