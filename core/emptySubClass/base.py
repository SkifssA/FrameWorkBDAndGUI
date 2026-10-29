from abc import ABC, abstractmethod

from core.package.DataFetcher import DataFetcher
from core.fabric.OperRegistry import OperRegistry
from core.package.MetadataManager import MetadataManager
from core.empty.logic import EmptyLogic
from core.dataClass.formEvent import formEvent
from core.context import current_session_id

class Base(ABC):
    def __init__(self, parentClass):
        self._parent_class = parentClass
        self.dataFetcher = DataFetcher(self)

        self.metaInfo = MetadataManager().get(
            parentClass.metaFile, self.__class__.__name__
        )
        self.registry = self._initRegistry()
        self._param = {}
        self._active_row = 0

    def thisLogic(self)->EmptyLogic:
        return self._parent_class.thisLogic()

    def thisObj(self):
        return self.dataFetcher._data[self._active_row]

    def getSelfAttr(self, nameAttr):
        res = self._get_form(nameAttr)
        if res['isNotValue']:
            res = self._get_param(nameAttr)

        return res

    def afterSetter(self, nameAttr):
        self.dataFetcher._obj(self.thisObj())
        return super().afterSetter(nameAttr)

    def _get_form(self, nameAttr):
        res = {
            'value' : None,
            'isNotValue': True
        }
        if (x:=self.dataFetcher.getData()) != []:
            if nameAttr in x[self._active_row]:
                res['value']  = x[self._active_row][nameAttr]
                res["isNotValue"] = False

        return res

    def _get_param(self, nameAttr):
        res = {
            'value' : None,
            'isNotValue': True
        }
        if nameAttr in self._param:
            res['value']  = self._param[nameAttr]
            res["isNotValue"] = False

        return res

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
        return self._get_parent_name()

    def _get_form_event(self, typeEvent: str):
        return formEvent(form=self.full_name()
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