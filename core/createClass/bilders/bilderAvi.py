from .bilderBase import BilderBase
from ...package import Core_FileManagerPkg

class BilderAvi(BilderBase):
    temp = """# Пользовательский файл для интерфейса
from core.formhandle.FornManeger import FormHandle, FornManeger
from .{nameClass}Dvi import {nameClass}Dvi

class {nameClass}Avi({nameClass}Dvi):
    class Tabl({nameClass}Dvi.DviTabl): pass

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

    async def createFileA(self, path):
        pathWhitFile = self._getPathAndFile(path)
        f = self.temp.format(**self.data)
        await Core_FileManagerPkg.CreateFile(pathWhitFile, f)
