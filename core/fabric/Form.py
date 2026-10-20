from typing import Any

from core.empty.pub import EmptyPub, eventSignal
from core.dataClass.formEvent import formEvent, typeEvent
from core.package.ModuleManagerPkg import ModuleManagerPkg

class Form:
    def __init__(self, cls: EmptyPub.Default, clsParent: EmptyPub):
        self.object: EmptyPub.Default = cls(clsParent)
        self.children:list[EmptyPub.Default] = []

    def _get_register_children(self):
        for i in self.object.metaInfo.tabCh:
            class_, sel  = i.split('.')
            class_obj = ModuleManagerPkg.getClassByName(class_)
            sel_obj = class_obj._getFormByName(sel)(class_obj)

    def getInfoMeta(self):
        return self.object._getInfoMeta()

    def getSetterAndOperName(self):
        return self.object._getSetterAndOperName()

    def getData(self):
        return self.object._getData()

    def get_oper_handler(self):
        return self.object.registry._flat_ops_handler

    def get_setter(self):
        return self.object.registry._flat_set_handler

    def _get_parent_name(self):
        return self.object._get_parent_name()

    def _get_full_name(self):
        return self.object.full_name()

    def param(self, nameParam: str, value: Any):
        self.object._param[nameParam] = value
        return self

    def close(self):
        eventSignal.send(fromEvent=self.object._get_form_event(typeEvent.closeForm))

    def open(self):
        event = self.object._get_form_event(typeEvent.openForm)
        event.formObject = self
        eventSignal.send(fromEvent=event)
        
