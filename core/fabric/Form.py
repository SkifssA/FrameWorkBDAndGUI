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

    def open(self):
        eventSignal.send(fromEvent=self.object._get_form_event(typeEvent.openForm))
