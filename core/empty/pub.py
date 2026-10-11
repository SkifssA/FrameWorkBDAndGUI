from abc import ABC, abstractmethod
from typing import Any

from core.package.DataFetcher import DataFetcher
from core.fabric.OperRegistry import OperRegistry
from core.package.MetadataManager import MetadataManager


class EmptyPub:
    metaFile: Any = ...
    thisLogic: Any = ...

    @classmethod
    def _getFormByName(cls, sForm: str) -> type["EmptyPub.Default"]:
        if x := getattr(cls, sForm.lower()):
            return x
        return None

    @classmethod
    def list(cls):
        from core.fabric.Form import Form

        return Form(cls.List, cls)

    class Default(ABC):
        def __init__(self, parentClass: "EmptyPub"):
            self._parent_class = parentClass
            self.dataFetcher = DataFetcher(self)
            self.metaInfo = MetadataManager().get(
                parentClass.metaFile, self.__class__.__name__
            )

            self.registry = self._initRegistry()

        def _getData(self):
            self.dataFetcher.refresh()
            return self.dataFetcher.getData()

        def _getInfoMeta(self):
            return {
                "operForm": self.registry.get_children_oper(),
                "metaForm": self.metaInfo.getDict(isNotNone=False),
            }

        def _getSetterAndOperName(self):
            return [
                i["id"] for i in self.registry.get_setter() + self.registry.get_oper()
            ]

        def _initRegistry(self) -> OperRegistry:
            registry = OperRegistry(self)
            registry.oper()
            registry.setter()
            return registry

        @abstractmethod
        def onRefresh(self): ...
        @abstractmethod
        def onRefreshExt(self): ...

        # @abstractmethod
        # def getAttr(self):...
        # @abstractmethod
        # def save(self):...
        # @abstractmethod
        # def delete(self):...

    class List(Default):
        def onRefresh(self):
            return self.structuredQuery()

        @abstractmethod
        def structuredQuery(self) -> str: ...
