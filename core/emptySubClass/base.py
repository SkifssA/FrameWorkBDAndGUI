from abc import ABC, abstractmethod
from typing import Any

from core.package.DataFetcher import DataFetcher
from core.fabric.OperRegistry import OperRegistry
from core.package.MetadataManager import MetadataManager
from core.empty.logic import EmptyLogic
from core.dataClass.formEvent import formEvent
from core.context import current_session_id
from core.context import eventSignal
from core.dataClass.type import typeEvent, typeLocat
from core.package.ModuleManagerPkg import ModuleManagerPkg

class Children:
    """Класс управление дочерними формами"""
    def __init__(self, parent: 'Base'):
        self.parent = parent
        self.init_meta_parent()

    def reset(self):
        """Инициализация переменных"""
        self._children:dict[str, 'Base'] = {}
        self.childrenMeta:dict[str, list['Base']] = {
            typeLocat.left: [],
            typeLocat.right: [],
            typeLocat.bottom: []
        }
        self.active_ch_bottom = 0

    def set_children(self, form: 'Base', locat=typeLocat.bottom):
        """Установка новой дочерней формы"""
        self._children[form.full_name()] = form
        self.childrenMeta[locat].append(form.getInfoMeta())

    def init_meta_parent(self):
        """Первичная инициализация из меты"""
        self.reset()
        for i in self.parent.metaInfo.tabsCh:
            class_, sel  = i.nameClass, i.repres
            class_obj = ModuleManagerPkg().getClassByName(class_)
            sel_obj:'Base' = class_obj._getFormByName(sel)(parentFrom=self.parent)
            self.set_children(sel_obj, i.location)

    def _get_children(self, form:str)->'Base':
        """????"""
        w = form.split('.')
        indexSelf = w.index(self.parent.full_name().split('.')[-1])
        if len(w) == 1 or indexSelf + 1 == len(w):
            return self
        
        ch = self._children[w[indexSelf + 1]]
        if len(w) > 2:
            return ch._children._get_children('.'.join(w[1:]))
        return ch

class Base(ABC):
    def __init__(self, parentClass, **kwargs):
        self._parent_class = parentClass
        self.dataFetcher = DataFetcher(self)
        self.metaInfo = MetadataManager().get(parentClass.metaFile, self.__class__.__name__)
        self._children = Children(self)
        self.parentForm:'Base' = kwargs.get('parentFrom')
        self.registry = self._initRegistry()
        self._param = {}
        self._active_row = 0
        self._attr_parent_refresh = []
        self.after_init()

    def setParentForm(self, parentForm):
        self.parentForm = parentForm
        self.metaInfo.name = self.full_name()

    def get_oper_handler(self):
        return self.registry._flat_ops_handler

    def get_setter(self):
        return self.registry._flat_set_handler

    @property
    def active_row(self):
        return self._active_row

    @active_row.setter
    def active_row(self, value):
        self._active_row = value
        self.validateDep()

    def validateDep(self):
        for key, val in self.children.items():
            for item in val._attr_parent_refresh:
                if (x:=val.getAttr(item['attr'])) != item['old_value']:
                    item['old_value'] = x
                    val.refresh()

    def thisLogic(self)->EmptyLogic:
        return self._parent_class.thisLogic()

    def thisObj(self):
        return self.dataFetcher._data[self._active_row]

    def getSelfAttr(self, nameAttr):
        res = self._get_form(nameAttr)
        if res['isNotValue']:
            res = self._get_param(nameAttr)

        return res

    def getAttr(self, nameAttr:str):
            prefix = nameAttr.split("$")[0]
            if prefix.lower() == 'super':
                return self.parentForm.getAttr(nameAttr[nameAttr.find("$")+1:])
    
            res = super().getSelfAttr(nameAttr)
            if res['isNotValue']:
                if self.parentForm is not None:
                    res = self.parentForm.getAttr(nameAttr)
    
            return res['value'] if isinstance(res, dict) else res

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
        
    def getData(self):
        return self.dataFetcher.getData()

    def getInfoMeta(self):
        metaForm = self.metaInfo.getDict(isNotNone=False)
        metaForm['name'] = self.full_name()
        metaForm['tabsCh'] = self.childrenMeta
        return {
            "operForm": self.registry.get_children_oper(),
            "setterForm": self.registry.setter(),
            "metaForm": metaForm,
        }

    def getSetterAndOperName(self):
        return [
            i["id"] for i in self.registry.get_setter() + self.registry.get_oper()
        ]

    def _get_parent_name(self):
        return self._parent_class.get_name()

    def full_name(self)->str:
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

    def close(self):
            eventSignal.send(fromEvent=self._get_form_event(typeEvent.closeForm))
    
    def refreshDown(self):
        self.dataFetcher.refresh()
        for key, value in self.children.items():
            value.refreshDown()

    def open(self):
        self.refreshDown()
        self._open_ui()

    def _open_ui(self):
        from core.package.SessionStageManager import SESSION_STAGE
        mm = SESSION_STAGE.get_app()
        mm._children[typeLocat.bottom] = self
        event = self._get_form_event(typeEvent.openForm)
        eventSignal.send(fromEvent=event)

    def _open_ch(self):
        event = self._get_form_event(typeEvent.open_form_ch)
        event.formObject = self
        eventSignal.send(fromEvent=event)

    def param(self, nameParam: str, value: Any):
        self._param[nameParam] = value
        return self

    def after_init(self):...

    @abstractmethod
    def onRefresh(self): ...
    @abstractmethod
    def onRefreshExt(self): ...