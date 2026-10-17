from typing import Any

from core.empty.pub import EmptyPub, eventSignal
from core.dataClass.formEvent import formEvent, typeEvent

class Form:
    def __init__(self, cls: EmptyPub.Default, clsParent: EmptyPub):
        self.object: EmptyPub.Default = cls(clsParent)

    def getInfoMeta(self):
        return self.object._getInfoMeta()

    def getSetterAndOperName(self):
        return self.object._getSetterAndOperName()

    def getData(self):
        return self.object._getData()

    def get_oper_handler(self):
        return self.object.registry._flat_ops_handler

    def _get_parent_name(self):
        return self.object._get_parent_name()

    def _get_full_name(self):
        return self.object.full_name()

    def param(self, nameParam: str, value: Any):
        self.object._param[nameParam] = value
        return self

    def open(self):
        if len(self.object.dataFetcher.getData()) == 0:
            self.object.dataFetcher.refresh()
        event = self.object._get_form_event(typeEvent.openForm)
        event.formObject = self
        eventSignal.send(fromEvent=event)
        
