import dearpygui.dearpygui as dpg
import importlib
import inspect

from ..package import ASQL
from engine.form.Base import Base
from engine.form.List import List
from engine.form.Card import Card
from engine.base.oper import SetOper
from engine.base.modal import DialogModal
from engine.base.Event import SetterEvent
from engine.base import api
from engine.fabric.Form import FormConstruct

class BaseAvi:

    @classmethod
    def typeMeta(cls, subClass, **kwargs):
        instance = subClass()
        # Устанавливаем атрибуты из kwargs
        for key, value in kwargs.items():
            setattr(instance, key, value)
        return instance
    
    @classmethod
    def list(cls, **kwargs)->FormConstruct: pass

    @classmethod
    def card(cls, **kwargs)->FormConstruct: pass

    def proccessById(self, event:SetterEvent, getAttr, setAttr, repList=None, repCard=None):
        if (event.type == 'selectValue'):
            selList = repList or self.__class__.list
            selList().openModal(
                callback=setAttr
            )
        elif (event.type == 'openCard'):
            selCard = repCard or self.__class__.card
            selCard(idItem=getAttr).openModal()
        elif (event.type == 'deleteValue'):
            setAttr({'id': None})
        else:
            print("Сеттер на ввод значения")

    class DefaultDefault(Base):
        def getAttr(self, name:str):
            w = name.split('$', maxsplit=1)
            n, p = w[0], '$'.join(w[1:])
            if n == 'super':
                if self.parent != 'tab_bar':
                    w:Base = dpg.get_item_user_data(self.parentTable)
                    return w.getAttr(p)  
            elif n == 'filter':
                return self.filter._getAttr(p)                           
            else:
                return self._getAttr(name)

        def thisApi(self)->api.BaseApi:
            return self._getAvi().thisApi()
        
        def _getAvi(self)->'BaseAvi':
            outer_class_name = self.__class__.__qualname__.rsplit('.', 1)[0]
            # Получаем имя модуля, где определён класс
            module_name = self.__class__.__module__
            module = importlib.import_module(module_name)
            return getattr(module, outer_class_name)
      
        
        @SetOper(label='Обновить', order=1, img='2')
        async def refreshForm(self):
            api.likeСache[self.thisApi()._getNameClass()] = {}
            self.rectUpdate()
            await self.refresh()

        @SetOper(label='Выбрать', order=-1, isVisible=False, img='10')
        async def returnResult(self):
            d = {}
            for i in self.returnAttr:
                d[i] = self.getAttr(i) 
            if self.callback is not None:
                if inspect.iscoroutinefunction(self.callback):
                    await self.callback(d)
                else:
                    self.callback(d)
            self.closeForm()

        def checwork(self):
            super().checwork()
            self.selection.oper('returnResult').isVisible = self.isModal

    class DefaultList(DefaultDefault, List):
        
        @SetOper(label='Открыть', order=2, img='4')
        async def openForm(self): self._getAvi().card().param(idItem=self.getAttr('id')).open()
        
        @SetOper(label='Создать', order=10, img='0')
        async def insert(self): self._getAvi().card().param(isInsert=True).open()

        @SetOper(label='Удалить', order=20, img='3')
        async def delete(self):
            await self.thisApi()._deleteById(self.getAttr('id'))
            await self.refresh()

        @SetOper(label='Закрыть', order=10000, img='1')
        async def closeFormCancel(self): self.closeForm()

        def thisRop(self):
            row = self.get_row()
            return self.thisApi()._createRop(row)

        def checwork(self):
            super().checwork()
            self.selection.oper(['openForm', 'delete']).isDisabled = self.getAttr('id') is None

    class DefaultCard(Card, DefaultDefault):

        async def open(self, parent='tab_bar', parentTable=None):
            if getattr(self, 'isInsert'):
                if self.isInsert:
                    obj = self.thisApi().insert()
                    setattr(self, 'idItem', obj.id)
            await super().open(parent, parentTable)

        @SetOper(label='Закрыть', order=10000, img='1')
        async def closeFormCancel(self):
            if not self.isModal:
                if self.isMod or self.isInsert:
                    DialogModal("Сохранить перед выходом?", self.handle_confirmation).show()
                else:
                    self.closeForm()
            else:
                if self.isInsert:
                    self.thisApi().delete(self.thisRop())
                self.closeForm()

        async def handle_confirmation(self, result: bool):
            if self.isInsert:
                if not result:
                    self.thisApi().delete(self.thisRop())
                else:
                    await self.saveForm()
            else:
                if result:
                    await self.saveForm()
            self.closeForm()

        @SetOper(label='Сохранить', order=1, img='5')
        async def saveForm(self):
            self.thisApi().update(self.thisRop())
            self.isInsert = False
            self.isMod = False

        @SetOper(label='Обновить', order=-1, img='2')
        async def refreshForm(self):
            await self.refresh()
        
        def checwork(self):
            super().checwork()
            self.selection.oper("saveForm").isDisabled = not self.isMod

        def onRefresh(self):
            return self.thisApi().load(self.idItem)

    class DefaultDet(DefaultDefault, List):
        def getIdMaster(self):
            return self.getAttr('super$id')

    class DefaultLookUp(DefaultDefault): 
        async def getData(self, tagMaster):
            self.parentTable = tagMaster
            self.rect.refresh()
            self.data = self.rect.getData()
            return self.data
        
        def getId(self, value:str)->int:
            return tuple(i['id'] for i in self.data if i['sHeadLine'] == value)[0]
        
        def _refresh(self):pass

        def _getAttr(self, name):pass

        def onRefreshExt(self):pass

        def createMainForm(self, par):pass

        