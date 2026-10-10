from abc import ABC, abstractmethod

from core.package.Rect import Rect
from core.fabric.Registry import Registry
from core.package.MetadataManager import MetadataManager

class EmptyPub:

    @classmethod
    def _getFormByName(cls, sForm:str)->type['Default']:
        if x:=getattr(cls, sForm):
            return x
        return None

    class Default(ABC):
        def __init__(self):
            self.rect = Rect(self)
            self.metaInfo = MetadataManager().get(self)

            self.registry = Registry(self)
            self.registry.oper()
            self.registry.setter()

        def getData(self):
            self.rect.refresh()
            return self.rect.getData()

        def getInfoMeta(self):
            return {
                'operForm': self.registry.get_children_oper()
                , 'metaForm': self.metaInfo.getDict(isNotNone=False)
            }

        @abstractmethod
        def onRefresh(self):...
        @abstractmethod
        def onRefreshExt(self):...
        @abstractmethod
        def getAttr(self):...
        @abstractmethod
        def save(self):...
        @abstractmethod
        def delete(self):...

    class List(Default):
        def onRefresh(self):
            return self.structuredQuery()
        
        @abstractmethod
        def structuredQuery(self)->str:...