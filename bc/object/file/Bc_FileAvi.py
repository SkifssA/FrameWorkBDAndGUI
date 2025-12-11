# Пользовательский файл для интерфейса
from .Bc_FileDvi import Bc_FileDvi
from core.empty.CardFileView import CardFileView
from core.base.BaseAvi import BaseAvi

class Bc_FileAvi(Bc_FileDvi):
    @classmethod
    def list(cls, **kwargs):
        return cls.typeMeta(cls.List, **kwargs)
    
    @classmethod
    def list_gidSrc(cls, **kwargs):
        return cls.typeMeta(cls.List_gidSrc, **kwargs)
    
    @classmethod
    def card(cls, **kwargs):
        return cls.typeMeta(cls.Card, **kwargs)

    class List(Bc_FileDvi.DviList):
        showAttr = ['sCaption', 'sSuffix']
        def openCh(self):
            yield Bc_FileAvi.CardFileView()

        def onRefresh(self):
            return super().onRefresh()

    class List_gidSrc(Bc_FileDvi.DviList):
        showAttr = ['sCaption', 'sSuffix']
        def openCh(self):
            yield Bc_FileAvi.CardFileView()

        async def onRefresh(self):
            return await super().onRefresh() + f"WHERE t.gidScr = '{self.getAttr("super$gid")}'"

    class Card(Bc_FileDvi.DviCard): pass

    class LookUp(Bc_FileDvi.DviLookUp): pass

    class CardFileView(CardFileView, BaseAvi.DefaultDefault):
        async def onRefresh(self):
            return await self.thisApi().getRealPath(self.getAttr('super$id'))
