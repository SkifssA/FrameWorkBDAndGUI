import importlib

from core.sdk import EmptyApi, EmptyObj, SetOper

from engineQT.ui.forms.base import Base as FormBase
from engineQT.ui.forms.list import List as FormList
from engineQT.ui.forms.card import Card as FormCard
from engineQT.ui.forms.mainmenu import MainMenu as FormMainMenu
from engineQT.fabric.Form import FormConstruct

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
            if (indSim:=sysName.find('$')) != -1: begin, end = sysName[:indSim], sysName[indSim+1:]
            else: begin, end = '', sysName

            attr = None
            if (begin == 'filter'): return self.filter._getAttr(end)
            if (begin != 'super'): attr = self.getSelfAttr(end)
            if attr is None and (x:=self.formParent) is not None:
                return x.getAttr(end)
            return attr

        def onRefresh(self):
            if self.filter and (x:=self.filter._getWhere()) != '':
                return f'{self.structuredQuery()} where {x}'
            return self.structuredQuery()

        def _onRefresh(self):
            super()._onRefresh()
            self.checwork()

        def structuredQuery(self)->str:...

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

        def thisRop(self)->EmptyObj:...

        def afterSetter(self, nameAttr):
            obj = self.thisRop()
            if (self.updateObj.get(str(obj)) is None):
                self.updateObj[str(obj)] = obj
            self.checwork()

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
                print(self.Rect.getData())
                self.Rect.refreshItem()
                print(self.Rect.getData())
                values = self.Rect.getData()[0]
                for item in self.Rect.getAttrExt():
                    self._setAttr(item, values[item])
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
        