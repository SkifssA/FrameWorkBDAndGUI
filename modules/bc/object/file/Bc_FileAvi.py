# Пользовательский файл для интерфейса
from .Bc_FileDvi import Bc_FileDvi
from core.form.CardFileView import CardFileView
from core.base.avi import BaseAvi

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
    def list(cls, **kwargs)->List:
        return cls.typeMeta(cls.List, **kwargs)
    
    @classmethod
    def list_gidSrc(cls, **kwargs)->List_gidSrc:
        return cls.typeMeta(cls.List_gidSrc, **kwargs)
    
    @classmethod
    def card(cls, **kwargs)->Card:
        return cls.typeMeta(cls.Card, **kwargs)
    
    @classmethod
    def cardFileView_idFile(cls, **kwargs)->CardFileView_idFile:
        return cls.typeMeta(cls.CardFileView_idFile, **kwargs)
    
    @classmethod
    def cardFileView_sUrl(cls, **kwargs)->CardFileView_sUrl:
        return cls.typeMeta(cls.CardFileView_sUrl, **kwargs)
