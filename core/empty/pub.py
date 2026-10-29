from abc import abstractmethod

from core.empty.logic import EmptyLogic
from core.dataClass.formEvent import typeEvent
from core.decorator.oper import Oper
from core.emptySubClass.base import Base as emptyBase
from core.emptySubClass.default import Default as emptyDefault
from core.context import eventSignal

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

    class Base(emptyBase):...

    class MainMenu(Base):
        def onRefreshExt(self): ""
        def onRefresh(self): ""

        @Oper(label='Приложение', order=-10)
        def project(self):...

        @Oper(label='Закрыть', order=10000, headOper='project')
        def closeProject(self):
            eventSignal.send(fromEvent=self._get_form_event(typeEvent.closeApp))

    class Default(emptyDefault, Base):
        def __init__(self, parentClass):
            super().__init__(parentClass)

            self.parentForm = None
            self._attr_parent_refresh = []
            
            self.after_init()

        def after_init(self):...

    class List(Default):   
        def onRefresh(self):
            return self.structuredQuery()

        @Oper(label="Создать запись", order=25)
        def insert(self):
            self._parent_class.card().param('idItem', self.thisLogic().insert().id).open()
        
        @Oper(label="Открыть карточку", order=30)
        def openCard(self):
            self._parent_class.card().param('idItem', self.getAttr('id')).open()

        @Oper(label="Удалить", order=40)
        def openCard(self):
            self.thisLogic().delete(self.thisLogic().load(self.getAttr('id')))
            self.refresh()

        @abstractmethod
        def structuredQuery(self) -> str: ...

    class Card(Default):
        def onRefresh(self):
            return self.thisLogic().load(self.getAttr('idItem'))

        @Oper(label="Сохранить", order=40)
        def saveForm(self):
            self.thisLogic().update(self.thisObj())

        def update_meta_form(self):
            super().update_meta_form()

            self.metaInfo.caption = self.thisLogic().calcHeadLine(self.thisObj())

        
