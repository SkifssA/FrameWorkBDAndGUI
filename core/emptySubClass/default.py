from core.dataClass.type import typeEvent
from core.decorator.oper import Oper
from core.context import eventSignal
from core.emptySubClass.base import Base
from core.dataClass.formRef import FormRef, CHR_SEPARATOR_PARENT

class Default(Base):    
    def addDepAttr(self, nameAttr:str):
        self._attr_parent_refresh.append({'attr':nameAttr, 'old_value': None})

    def name(self):
        return FormRef.create(self._get_parent_name(), self.__class__.__name__).getStr()

    @Oper(label='Обновить', order=10)
    def refresh(self):
        self._refresh()
        eventSignal.send(fromEvent=self._get_form_event(typeEvent.refresh))

    def _refresh(self):
        self.dataFetcher.refresh()
        self.update_meta_form()

    def update_meta_form(self):...
    def afterSetter(self, nameAttr):...