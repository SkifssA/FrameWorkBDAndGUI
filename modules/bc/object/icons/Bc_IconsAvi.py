# Пользовательский файл для интерфейса
from .Bc_IconsDvi import Bc_IconsDvi
from core.empty.CardFileView import CardFileView
from core.base.avi import BaseAvi
from core.package import Core_FileManagerPkg
from core.formhandle.FornManeger import FormHandle, FornManeger

class Bc_IconsAvi(Bc_IconsDvi):
    class List(Bc_IconsDvi.DviList): 
        def openCh(self):
            yield Bc_IconsAvi.cardFileView_idFile()

    class Card(Bc_IconsDvi.DviCard): pass

    class LookUp(Bc_IconsDvi.DviLookUp): pass

    class CardFileView_idFile(CardFileView, BaseAvi.DefaultDefault):
        def onRefresh(self):
            return Core_FileManagerPkg._getObjPath(self.getAttr('super$sPath'))

    @classmethod
    def list(cls)->FormHandle:
        return FornManeger.register(cls.List)
    
    @classmethod
    def card(cls)->FormHandle:
        return FornManeger.register(cls.Card)
    
    @classmethod
    def cardFileView_idFile(cls)->FormHandle:
        return FornManeger.register(cls.CardFileView_idFile)
