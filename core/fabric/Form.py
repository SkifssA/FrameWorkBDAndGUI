from typing import Any

from core.empty.pub import EmptyPub, eventSignal
from core.dataClass.formEvent import formEvent, typeEvent
from core.package.ModuleManagerPkg import ModuleManagerPkg

class Form:
    def __init__(self, cls: EmptyPub.Default, clsParent: EmptyPub, **kwargs):
        self.object: EmptyPub.Default = cls(clsParent)
        if 'parentFrom' in kwargs:
            self.object.setParentForm(kwargs['parentFrom'])
            
        self.children:dict[str, 'Form'] = {}
        self._get_register_children()
        self.childrenMeta:list = list(i.getInfoMeta() for i in self.children.values())
        self.active_ch = 1

    def _get_register_children(self):
        self.object.dataFetcher.refresh()
        for i in self.object.metaInfo.tabCh:
            class_, sel  = i.split('/')
            class_obj = ModuleManagerPkg().getClassByName(class_)
            sel_obj:'Form' = class_obj._getFormByName(sel)(parentFrom=self.object)
            self.children[sel_obj.object.name()] = sel_obj

    def _get_children(self, form:str)->'Form':
        w = form.split('.')
        if len(w) == 1:
            return self
        
        ch = self.children[w[1]]
        if len(w) > 2:
            return ch._get_children('.'.join(w[1:]))
        return ch


    def getInfoMeta(self):
        m = self.object._getInfoMeta()
        m['metaForm']['tabCh'] = self.childrenMeta
        return m

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

    def open_ch(self):
        event = self.object._get_form_event(typeEvent.open_form_ch)
        event.formObject = self
        eventSignal.send(fromEvent=event)
        
