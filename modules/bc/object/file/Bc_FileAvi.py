# Пользовательский файл для интерфейса
from .Bc_FileDvi import Bc_FileDvi
from core.form.CardFileViewFlet import CardFileView
from core.base.avi import BaseAvi
from core.formhandle.FornManeger import FormHandle, FornManeger

class Bc_FileAvi(Bc_FileDvi):
    class List(Bc_FileDvi.DviList):
        def openCh(self):
            yield Bc_FileAvi.cardFileView_idFile()

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
        def onRefresh(self):
            return self.thisApi().getRealPath(self.getAttr('super$id'))
        
    class CardFileView_sUrl(CardFileView, BaseAvi.DefaultDefault):
        def onRefresh(self):
            return {'real_path':self.getAttr("super$sUrlImg"), 'type':'http'}
        
    @classmethod
    def list(cls)->FormHandle:
        return FornManeger.register(cls.List)
    
    @classmethod
    def card(cls)->FormHandle:
        return FornManeger.register(cls.Card)
    
    @classmethod
    def list_gidSrc(cls)->FormHandle:
        return FornManeger.register(cls.List_gidSrc)
    
    @classmethod
    def cardFileView_idFile(cls)->FormHandle:
        return FornManeger.register(cls.CardFileView_idFile)
    
    @classmethod
    def cardFileView_sUrl(cls)->FormHandle:
        return FornManeger.register(cls.CardFileView_sUrl)
