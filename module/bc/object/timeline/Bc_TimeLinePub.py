# Пользовательский файл для интерфейса
from dataclasses import dataclass

from .Bc_TimeLineDvi import Bc_TimeLineDvi
from module.bc.object.scheduledtasks.Bc_ScriptSchedulerPub import Bc_ScriptSchedulerPub
from core.sdk import Oper, Setter, BaseDataClass


class Bc_TimeLinePub(Bc_TimeLineDvi):
    metaFile = "Bc_TimeLine.Ameta.json"

    class List(Bc_TimeLineDvi.DviList):
        @Setter
        def setsCaption(self):
            pass

    class Card(Bc_TimeLineDvi.DviCard):
        pass

    class TextCard(Bc_TimeLineDvi.DviCard):
        def after_init(self):
            super().after_init()
            self.addDepAttr('super$id')

        def onRefresh(self):
            return self.thisLogic().load(self.getAttr('super$id'))

    class ImgCard(Bc_TimeLineDvi.DviCard):
        @dataclass
        class Img(BaseDataClass):
            urlImg: str

        def onRefresh(self):
            return self.Img(urlImg='https://img.cdngos.com/anime/6a/6ab39ccfc3d3a105557463')

        def onRefreshExt(self): return ''

    class LookUp(Bc_TimeLineDvi.DviLookUp):
        pass

    @classmethod
    def list(cls, **kwargs):
        return cls.List(cls, **kwargs)

    @classmethod
    def card(cls, **kwargs):
        return cls.Card(cls, **kwargs)

    @classmethod
    def textCard(cls, **kwargs):
        return cls.TextCard(cls, **kwargs)

    @classmethod
    def imgCard(cls, **kwargs):
        return cls.ImgCard(cls, **kwargs)
