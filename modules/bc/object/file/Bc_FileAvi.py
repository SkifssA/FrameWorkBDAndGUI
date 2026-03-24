# Пользовательский файл для интерфейса
from .Bc_FileDvi import Bc_FileDvi
from core.empty.CardFileViewFlet import CardFileView
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

        async def onRefresh(self):
            return await super().onRefresh() + f"WHERE t.gidScr = :super$gid"

    class Card(Bc_FileDvi.DviCard): pass

    class LookUp(Bc_FileDvi.DviLookUp): pass

    class CardFileView_idFile(CardFileView, BaseAvi.DefaultDefault):
        async def onRefresh(self):
            return await self.thisApi().getRealPath(self.getAttr('super$id'))
        
    class CardFileView_sUrl(CardFileView, BaseAvi.DefaultDefault):
        async def onRefresh(self):
            return {'real_path':self.getAttr("super$sUrlImg"), 'type':'http'}
        
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
    def cardFileView_sUrl(cls)->FormHandle:
        return FornManeger.register(cls.CardFileView_sUrl)
