from abc import ABC, abstractmethod
from blinker import signal

from core.package.DataFetcher import DataFetcher
from core.fabric.OperRegistry import OperRegistry
from core.package.MetadataManager import MetadataManager
from core.empty.logic import EmptyLogic
from core.dataClass.formEvent import formEvent, typeEvent
from core.decorator.oper import Oper
from core.context import current_session_id


eventSignal = signal('form-all-events')

class EmptyPub:
    metaFile: str
    thisLogic: EmptyLogic

    @classmethod
    def _getFormByName(cls, sForm: str) -> type["EmptyPub.Default"]:
        if x := getattr(cls, sForm.lower()):
            return x
        return None

    @classmethod
    def list(cls):
        from core.fabric.Form import Form

        return Form(cls.List, cls)

    @classmethod
    def get_name(cls)->str:
        return cls.__name__

    class Base(ABC):
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
            metaForm = self.metaInfo.getDict(isNotNone=False)
            metaForm['name'] = f'{self._parent_class.get_name()}/{metaForm['name']}'
            return {
                "operForm": self.registry.get_children_oper(),
                "metaForm": metaForm,
            }

        def _getSetterAndOperName(self):
            return [
                i["id"] for i in self.registry.get_setter() + self.registry.get_oper()
            ]

        def _get_parent_name(self):
            return self._parent_class.get_name()

        def _get_form_event(self, typeEvent: str):
            return formEvent(form=f'{self._get_parent_name()}/{self.__class__.__name__}'
                             , type=typeEvent
                             , session_id=current_session_id.get())

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

    class MainMenu(Base):
        def onRefreshExt(self): ""
        def onRefresh(self): ""

        def _get_form_event(self, typeEvent: str):
            return formEvent(form=f'{self._get_parent_name()}'
                                , type=typeEvent
                                , session_id=current_session_id.get())

        @Oper(label='Приложение', order=-10)
        def project(self):...

        @Oper(label='Закрыть', order=10000, headOper='project')
        def closeProject(self):
            eventSignal.send(fromEvent=self._get_form_event(typeEvent.closeApp))

    class Default(Base):
        @Oper(label='Обновить', order=10)
        def refresh(self):
            eventSignal.send(fromEvent=self._get_form_event(typeEvent.openForm))

    class List(Default):
        def onRefresh(self):
            return self.structuredQuery()

        @abstractmethod
        def structuredQuery(self) -> str: ...
