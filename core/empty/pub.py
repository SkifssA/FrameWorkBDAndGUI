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
    def _getFormByName(cls, sForm: str) -> object:
        sFormZero = sForm.split('?')[0]
        sFormZero = sFormZero[0].lower() + sFormZero[1:]
        if x := getattr(cls, sFormZero):
            return x
        return None

    @classmethod
    def list(cls, **kwargs):
        from core.fabric.Form import Form

        return Form(cls.List, cls, **kwargs)

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
            self._param = {}
            self._fun_validate_dep = None

        def reg_fun_validate_dep(self, fun):
            self._fun_validate_dep = fun

        def thisLogic(self)->EmptyLogic:
            return self._parent_class.thisLogic()

        def getAttr(self, nameAttr):
            res = self._get_form(nameAttr)
            if res is None:
                res = self._get_param(nameAttr)

            return res

        def _get_form(self, nameAttr):
            if (x:=self.dataFetcher.getData()) != []:
                return x[0].get(nameAttr)

        def _get_param(self, nameAttr):
            return self._param.get(nameAttr)

        def _get_parent(self, nameAttr):
            if self.parent:
                return self.parent.getAttr(nameAttr)
            
        def _getData(self):
            return self.dataFetcher.getData()

        def _getInfoMeta(self):
            metaForm = self.metaInfo.getDict(isNotNone=False)
            metaForm['name'] = self.full_name()
            return {
                "operForm": self.registry.get_children_oper(),
                "setterForm": self.registry.setter(),
                "metaForm": metaForm,
            }

        def _getSetterAndOperName(self):
            return [
                i["id"] for i in self.registry.get_setter() + self.registry.get_oper()
            ]

        def _get_parent_name(self):
            return self._parent_class.get_name()

        def full_name(self):
            return f'{self._get_parent_name()}/{self.__class__.__name__}{f'?id={x}' if (x:=self.getAttr('idItem')) else ''}'

        def _get_form_event(self, typeEvent: str):
            return formEvent(form=self.full_name()
                             , type=typeEvent
                             , session_id=current_session_id.get())

        def _initRegistry(self) -> OperRegistry:
            registry = OperRegistry(self)
            registry.oper()
            registry.setter()
            return registry

        def after_init(self):...

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

        def full_name(self):
            return self._get_parent_name()

        @Oper(label='Приложение', order=-10)
        def project(self):...

        @Oper(label='Закрыть', order=10000, headOper='project')
        def closeProject(self):
            eventSignal.send(fromEvent=self._get_form_event(typeEvent.closeApp))

    class Default(Base):
        def __init__(self, parentClass):
            super().__init__(parentClass)
            self.parentForm = None

            self._attr_parent_refresh = []
            
            self.after_init()

        

        def getAttr(self, nameAttr:str):
            prefix = nameAttr.split("$")[0]
            if prefix.lower() == 'super':
                return self.parentForm.getAttr(nameAttr[nameAttr.find("$")+1:])

            res = super().getAttr(nameAttr)
            if res is None:
                res = self.parentForm.getAttr(nameAttr)

            return res

        def addDepAttr(self, nameAttr:str):
            self._attr_parent_refresh.append({'attr':nameAttr, 'old_value': None})

        def setParentForm(self, parentForm):
            self.parentForm = parentForm
            self.metaInfo.name = self.full_name()

        def full_name(self):
            return f'{self.parentForm.full_name() + '.' if self.parentForm else ''}{self.name()}'

        def name(self):
            return f'{self._get_parent_name()}/{self.__class__.__name__}'

        @Oper(label='Обновить', order=10)
        def refresh(self):
            self._refresh()
            eventSignal.send(fromEvent=self._get_form_event(typeEvent.refresh))

        def _refresh(self):
            self.dataFetcher.refresh()
            self.update_meta_form()

        def update_meta_form(self):...
        def afterSetter(self, nameAttr):...
        def thisObj(self):...

    class List(Default):
        def __init__(self, parentClass):
            super().__init__(parentClass)
            self._active_row = 1

        @property
        def active_row(self):
            return self._active_row

        @active_row.setter
        def active_row(self, value):
            self._active_row = value
            if self._fun_validate_dep:
                self._fun_validate_dep()
            
        def _get_form(self, nameAttr):
            if (x:=self.dataFetcher.getData()) != []:
                if ((y:=list(i for i in x if i.get('id') == self.active_row)) != []):
                    return y[-1].get(nameAttr)

        @Oper(label="Открыть карточку", order=30)
        def openCard(self):
            self._parent_class.card().param('idItem', self.getAttr('id')).open()

        def onRefresh(self):
            return self.structuredQuery()

        @abstractmethod
        def structuredQuery(self) -> str: ...

    class Card(Default):
        def onRefresh(self):
            return self.thisLogic().load(self.getAttr('idItem'))

        def afterSetter(self, nameAttr):
            self.dataFetcher._obj(self.thisObj())
            return super().afterSetter(nameAttr)

        def thisObj(self):
            return self.dataFetcher._obj_res

        def update_meta_form(self):
            super().update_meta_form()

            self.metaInfo.caption = self.thisLogic().calcHeadLine(self.thisObj())

        
