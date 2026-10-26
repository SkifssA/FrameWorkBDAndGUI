from typing import Any

from core.empty.pub import EmptyPub, eventSignal
from core.dataClass.formEvent import formEvent, typeEvent
from core.package.ModuleManagerPkg import ModuleManagerPkg

class Form:
    def __init__(self, cls: EmptyPub.Default, clsParent: EmptyPub, **kwargs):
        self.object: EmptyPub.Default = cls(clsParent)
        self.object.reg_fun_validate_dep(self.validateDep)
        if 'parentFrom' in kwargs:
            self.object.setParentForm(kwargs['parentFrom'])
            
        self.children:dict[str, 'Form'] = {}
        self.childrenMeta:dict[str, list] = {}
        self._get_register_children()
        self.active_ch = 1

    def validateDep(self):
        for key, val in self.children.items():
            for item in val.object._attr_parent_refresh:
                if (x:=val.object.getAttr(item['attr'])) != item['old_value']:
                    item['old_value'] = x
                    val.object.refresh()

    def _get_register_children(self):
        self.childrenMeta = {
            'left': [],
            'right': [],
            'bottom': []
        }
        for i in self.object.metaInfo.tabsCh:
            class_, sel  = i.nameClass, i.repres
            class_obj = ModuleManagerPkg().getClassByName(class_)
            sel_obj:'Form' = class_obj._getFormByName(sel)(parentFrom=self.object)
            self.children[sel_obj.object.name()] = sel_obj
            self.childrenMeta[i.location].append(sel_obj.getInfoMeta())

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
        m['metaForm']['tabsCh'] = self.childrenMeta
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

    def refreshDown(self):
        self.object.dataFetcher.refresh()
        for key, value in self.children.items():
            value.refreshDown()

    def open(self):
        self.refreshDown()
        self._open_iu()

    def _open_iu(self):
        event = self.object._get_form_event(typeEvent.openForm)
        event.formObject = self
        eventSignal.send(fromEvent=event)

    def _open_ch(self):
        event = self.object._get_form_event(typeEvent.open_form_ch)
        event.formObject = self
        eventSignal.send(fromEvent=event)
        
