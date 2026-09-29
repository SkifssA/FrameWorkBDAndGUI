import importlib

from core.ui.forms.base import Base as FormBase
from core.ui.forms.list import List as FormList
from core.ui.forms.card import Card as FormCard
from core.ui.forms.mainmenu import MainMenu as FormMainMenu
from core.ui.widget.menubar import SetOper
from core.empty.api import EmptyApi
from core.fabric.Form import FormConstruct

class EmptyAvi:

    @classmethod
    def list(cls): return FormConstruct(cls.List)
    @classmethod
    def card(cls): return FormConstruct(cls.Card)

    class Base(FormBase):
        def afterOpen(self):...

        def getSelfAttr(self, sysName:str):
            return self._getAttr(sysName)
            
        def getAttr(self, sysName:str):
            attr = self.getSelfAttr(sysName)
            if attr is None and (x:=self.formParent) is not None:
                return x.getAttr(sysName)
            return attr

        def _onRefresh(self):
            super()._onRefresh()
            self.checwork()

    class MainMenu(Base, FormMainMenu):
        def oneOpen(self):...

    class Default(Base):
        def __init__(self, **kwargs):
            self.updateObj = {}
            super().__init__(**kwargs)

        @SetOper("Сохранить", icon='save.png', order=-5)
        def saveForm(self):
            for obj in self.updateObj.values():
                self.thisApi().update(obj)
            self.updateObj = {}
            self.refreshForm()

        @SetOper("Обновить", icon='update.png', order=-4)
        def refreshForm(self):
            self._onRefresh()

        @SetOper("Закрыть", order=1000, icon='close.png')
        def closeForm(self):
            self.formParent.close(self.caption)

        def thisApi(self)->EmptyApi:
            return self._getAvi().thisApi()

        def thisRop(self):...

        def afterSetter(self):
            obj = self.thisRop()
            if (self.updateObj.get(str(obj), None) is None):
                self.updateObj[str(obj)] = obj

        def _getAvi(self)->'EmptyAvi':
            outer_class_name = self.__class__.__qualname__.rsplit('.', 1)[0]
            # Получаем имя модуля, где определён класс
            module_name = self.__class__.__module__
            module = importlib.import_module(module_name)
            return getattr(module, outer_class_name)

        def checwork(self):
            super().checwork()
            self.oper.isEnabled(['saveForm', ], len(self.updateObj) > 0)

    class List(Default, FormList):
        @SetOper("Открыть карточку", icon='open.png', order=-3)
        def editCard(self):
            self._getAvi().card().param(idItem=self.thisRop().id).openForm()

        @SetOper("Удалить", icon='delete.png')
        def delete(self):
            self.thisApi().delete(self.thisRop())
            self._onRefresh()

        def thisRop(self):
            if (obj:=self._getUserData('id')):
                return obj
            obj = self.thisApi().load(self.getSelfAttr('id'))
            self._setUserData('id', obj)
            return obj            

    class Card(Default, FormCard):
        def thisRop(self):
            return self.obj

        def afterOpen(self):
            self.caption = self.thisApi().calcHeadLine(self.thisRop())
            return super().afterOpen()

        def _onRefresh(self):
            if self.updateObj.get(str(self.thisRop())):
                self.Rect.refreshItem()
                values = self.Rect.getData()[0]
                for item, value in self._editors.items():
                    value.setValue(values[item])
            else:
                super()._onRefresh()

    class LookUp:
        def __init__(self):
            from core.package.Rect import Rect
            self.rect = Rect(self)

        def getData(self):
            self.rect.refresh()
            self.data = self.rect.getData()
            return self.data