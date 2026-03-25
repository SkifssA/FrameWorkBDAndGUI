import dearpygui.dearpygui as dpg

import inspect

from ..package import ASQL
from ..empty.FormFlet import BaseForm
from ..empty.ListFlet import EmptyList
from ..empty.EmptyCard import EmptyCard
from .oper import SetOper
from .modal import DialogModal
from .Event import SetterEvent
from core.base.api import BaseApi

class BaseAvi:

    @classmethod
    def typeMeta(cls, subClass, **kwargs):
        instance = subClass()
        setattr(instance, 'locat', 'bottom')
        # Устанавливаем атрибуты из kwargs
        for key, value in kwargs.items():
            setattr(instance, key, value)
        return instance
    
    @classmethod
    def list(cls, **kwargs): pass

    @classmethod
    def card(cls, **kwargs): pass

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

    class DefaultDefault(BaseForm):
        def getAttr(self, name:str):
            w = name.split('$', maxsplit=1)
            n, p = w[0], '$'.join(w[1:])
            if n == 'super':
                if self.parentTabs is not None:
                    w:BaseForm = self.parentTabs.data
                    return w.getAttr(p)  
            elif n == 'filter':
                return self.filter._getAttr(p)                           
            else:
                return self._getAttr(name)

        def thisApi(self)->BaseApi:
            return self._getAvi().thisApi()
      
        
        @SetOper(label='Обновить', order=1)
        async def refreshForm(self): self.refresh()

        @SetOper(label='Выбрать', order=-1, isVisible=False)
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

    class DefaultList(DefaultDefault, EmptyList):
        
        @SetOper(label='Открыть', order=2)
        async def openForm(self): await self._getAvi().card(idItem=self.getAttr('id')).open()
        
        @SetOper(label='Создать', order=10)
        async def insert(self): await self._getAvi().card(isInsert=True).open()

        @SetOper(label='Удалить', order=20)
        async def delete(self):
            await self.thisApi()._deleteById(self.getAttr('id'))
            self.refresh()

        @SetOper(label='Закрыть', order=10000)
        async def closeFormCancel(self): self.close()

        def thisRop(self):
            row = self.get_row()
            return self.thisApi()._createRop(row)

        def checwork(self):
            super().checwork()
            self.selection.oper(['openForm', 'delete']).isDisabled = self.getAttr('id') is None

    class DefaultCard(DefaultDefault, EmptyCard): 
        @SetOper(label='Закрыть', order=10000)
        async def closeFormCancel(self):
            if not self.isModal:
                if self.isMod or self.isInsert:
                    DialogModal("Сохранить перед выходом?", self.handle_confirmation).show()
                else:
                    self.closeForm()
            else:
                if self.isInsert:
                    await self.thisApi().delete(self.obj)
                self.closeForm()

        def thisRop(self):
            return self.obj

        async def handle_confirmation(self, result: bool):
            if self.isInsert:
                if not result:
                    await self.thisApi().delete(self.obj)
                else:
                    await self.saveForm()
            else:
                if result:
                    await self.saveForm()
            self.closeForm()

        @SetOper(label='Сохранить', order=1)
        async def saveForm(self):
            await self.thisApi().update(self.obj)
            self.isInsert = False
            self.isMod = False

        @SetOper(label='Обновить', order=-1)
        async def refreshForm(self):
            await self.refresh()

        async def afterCreate(self):
            # await self.refresh()
            pass

        async def _refresh(self):
            self.obj = await self.getObj()
            await self.initInput()
            self.checwork()
            
        async def getObj(self):
            if self.obj is None:
                if getattr(self, 'idItem', None) is None:
                    obj = await self.thisApi().insert()
                    setattr(self, 'idItem', obj.id)
                    return obj
                return await self.thisApi().load(getattr(self, 'idItem', None))
            return self.obj
        
        def checwork(self):
            super().checwork()
            self.selection.oper("saveForm").isDisabled = not self.isMod

    class DefaultDet(DefaultDefault, EmptyList):
        def getIdMaster(self):
            return self.getAttr('super$id')

    class DefaultLookUp(DefaultDefault): 
        async def getData(self, tagMaster):
            self.parentTable = tagMaster
            self.data = await ASQL(*self.getSqlAndParam(await self.onRefresh()))
            return self.data
        
        def getId(self, value:str)->int:
            return tuple(i['id'] for i in self.data if i['sHeadLine'] == value)[0]
        
        def _refresh(self):pass

        def _getAttr(self):pass

        def onRefreshExt(self):pass

        def createMainForm(self, par):pass

        