# Пользовательский файл для интерфейса
from .Bc_IconsDvi import Bc_IconsDvi
from core.form.CardFileView import CardFileView
from core.base.avi import BaseAvi
from core.package import Core_FileManagerPkg
from core.fabric.Form import FormConstruct

class Bc_IconsAvi(Bc_IconsDvi):
    class List(Bc_IconsDvi.DviList): 
        def openCh(self):
            yield Bc_IconsAvi.cardFileView_idFile()

    class Card(Bc_IconsDvi.DviCard): pass

    class LookUp(Bc_IconsDvi.DviLookUp): pass

    class CardFileView_idFile(CardFileView, BaseAvi.DefaultDefault):
        class Data:
            def __init__(self):
                self.real_path = None
                self.type = None


        def onRefresh(self):
            w = self.Data()
            q:dict = Core_FileManagerPkg._getObjPath(self.getAttr('super$sPath'))
            w.real_path = q.get('real_path', None)
            w.type = q.get('type', None)
            return w

    @classmethod
    def list(cls)->FormConstruct:
        return FormConstruct(cls.List)
    
    @classmethod
    def card(cls)->FormConstruct:
        return FormConstruct(cls.Card)
    
    @classmethod
    def cardFileView_idFile(cls)->FormConstruct:
        return FormConstruct(cls.CardFileView_idFile)
