# Пользовательский файл для интерфейса
from .Bc_IconsDvi import Bc_IconsDvi
from core.empty.CardFileView import CardFileView
from core.base.BaseAvi import BaseAvi
from core.package import Core_FileManagerPkg

class Bc_IconsAvi(Bc_IconsDvi):
    class List(Bc_IconsDvi.DviList): 
        def openCh(self):
            yield Bc_IconsAvi.cardFileView_idFile()

    class Card(Bc_IconsDvi.DviCard): pass

    class LookUp(Bc_IconsDvi.DviLookUp): pass

    class CardFileView_idFile(CardFileView, BaseAvi.DefaultDefault):
        async def onRefresh(self):
            return Core_FileManagerPkg._getObjPath(self.getAttr('super$sPath'))

    @classmethod
    def list(cls, **kwargs)->List:
        return cls.typeMeta(cls.List, **kwargs)
    
    @classmethod
    def card(cls, **kwargs)->Card:
        return cls.typeMeta(cls.Card, **kwargs)
    
    @classmethod
    def cardFileView_idFile(cls, **kwargs)->CardFileView_idFile:
        return cls.typeMeta(cls.CardFileView_idFile, **kwargs)
