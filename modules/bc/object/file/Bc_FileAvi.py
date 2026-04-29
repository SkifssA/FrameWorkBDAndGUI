# Пользовательский файл для интерфейса
from .Bc_FileDvi import Bc_FileDvi
from engine.form.CardFileView import CardFileView
from engine.base.avi import BaseAvi
from engine.fabric.Form import FormConstruct

class Bc_FileAvi(Bc_FileDvi):
    class List(Bc_FileDvi.DviList):
        def openCh(self):
            yield Bc_FileAvi.CardFileView_idFile()

        def onRefresh(self):
            return super().onRefresh()

    class List_gidSrc(Bc_FileDvi.DviList):
        def openCh(self):
            yield Bc_FileAvi.cardFileView_idFile()

        def onRefresh(self):
            return super().onRefresh() + f"WHERE t.gidScr = :super$gid"

    class Card(Bc_FileDvi.DviCard): pass

    class LookUp(Bc_FileDvi.DviLookUp): pass

    class CardFileView_idFile(CardFileView, BaseAvi.DefaultDefault):
        class Data:
            def __init__(self):
                self.real_path = None
                self.type = None

        def onRefresh(self):
            w = self.Data()
            q:dict = self.thisApi().getRealPath(self.getAttr('super$id'))
            w.real_path = q.get('real_path', None)
            w.type = q.get('type', None)
            return w
        
    class CardFileView_sUrl(CardFileView, BaseAvi.DefaultDefault):
        class Data:
            def __init__(self):
                self.real_path = None
                self.type = None

        def onRefresh(self):
            w = self.Data()
            w.real_path = self.getAttr("super$sUrlImg")
            w.type = 'http'
            return w 
        
    @classmethod
    def list(cls)->FormConstruct:
        return FormConstruct(cls.List)
    
    @classmethod
    def list_gidSrc(cls)->FormConstruct:
        return FormConstruct(cls.List_gidSrc)
    
    @classmethod
    def card(cls)->FormConstruct:
        return FormConstruct(cls.Card)
    
    @classmethod
    def cardFileView_idFile(cls, **kwargs)->FormConstruct:
        return FormConstruct(cls.CardFileView_idFile)
    
    @classmethod
    def cardFileView_sUrl(cls)->FormConstruct:
        return FormConstruct(cls.CardFileView_sUrl)
