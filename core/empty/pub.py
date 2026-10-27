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

        def full_name(self):
            return self._get_parent_name()

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
        def __init__(self, parentClass):
            super().__init__(parentClass)
            self._active_row = 1

        @property
        def active_row(self):
            return self._active_row

        @active_row.setter
        def active_row(self, value):
            self._active_row = value
            
        def _get_form(self, nameAttr):
            res = {
                'value' : None,
                'isNotValue': True
            }
            if (x:=self.dataFetcher.getData()) != []:
                if ((y:=list(i for i in x if i.get('id') == self.active_row)) != []):
                    if nameAttr in y[-1]:
                        res['value']  = y[-1].get(nameAttr)
                        res["isNotValue"] = False

            return res
        
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

        @Oper(label="Сохранить", order=40)
        def saveForm(self):
            self.thisLogic().update(self.thisObj())

        def update_meta_form(self):
            super().update_meta_form()

            self.metaInfo.caption = self.thisLogic().calcHeadLine(self.thisObj())

        
