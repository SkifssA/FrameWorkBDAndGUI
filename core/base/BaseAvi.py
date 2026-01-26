import dearpygui.dearpygui as dpg
import importlib

from ..package import ASQL
from ..empty.BaseForm import BaseForm
from ..empty.EmptyList import EmptyList
from ..empty.EmptyCard import EmptyCard
from .BaseOper import SetOper
from .BaseModal import BaseModal

class BaseAvi:

    @classmethod
    def typeMeta(cls, subClass, **kwargs):
        instance = subClass()
        # Устанавливаем атрибуты из kwargs
        for key, value in kwargs.items():
            setattr(instance, key, value)
        return instance

    class DefaultDefault(BaseForm):
        def getAttr(self, name:str):
            if name.split('$', maxsplit=1)[0] == 'super':
                if self.parent != 'tab_bar':
                    w:BaseForm = dpg.get_item_user_data(self.parentTable)
                    return w._getAttr(name.split('$')[-1])                             
            else:
                row = self._getAttr(name)
                return row

        async def thisRop(self):
            row = self.get_row()
            return await self.thisApi()._createRop(row)

        def thisApi(self):
            return self._getAvi().thisApi()
        
        def _getAvi(self):
            outer_class_name = self.__class__.__qualname__.rsplit('.', 1)[0]
            # Получаем имя модуля, где определён класс
            module_name = self.__class__.__module__
            module = importlib.import_module(module_name)
            return getattr(module, outer_class_name)
      
    class DefaultList(DefaultDefault, EmptyList):

        @SetOper(label='Выбрать', order=-1, isVisible=False)
        async def returnResult(self):
            d = {}
            for i in self.returnAttr:
                d[i] = self.getAttr(i) 
            self.callback(**d)
            dpg.hide_item(self.tab)

        @SetOper(label='Обновить', order=1)
        async def refreshForm(self): await self.refresh()

        @SetOper(label='Открыть', order=2)
        async def openForm(self): await self._getAvi().card(idItem=self.getAttr('id')).open()
        
        @SetOper(label='Создать', order=10)
        async def insert(self): await self._getAvi().card(isInsert=True).open()

        @SetOper(label='Удалить', order=20)
        async def delete(self):
            await self.thisApi()._deleteById(self.getAttr('id'))
            await self.refresh()

        @SetOper(label='Закрыть', order=10000)
        async def closeForm(self): self.deleteItem()


        def checwork(self):
            super().checwork()
            print(self.getAttr('id'))
            self.selection.oper(['openForm', 'delete']).isDisabled = self.getAttr('id') is None
            self.selection.oper('returnResult').isVisible = self.isModal

    class DefaultCard(DefaultDefault, EmptyCard): 

        @SetOper(label='Выбрать', order=-1, isVisible=False)
        async def returnResult(self):
            d = {}
            for i in self.returnAttr:
                d[i] = self.getAttr(i) 
            await self.callback(**d)
            dpg.hide_item(self.tab)

        @SetOper(label='Закрыть', order=10000)
        async def closeForm(self):
            if not self.isModal:
                if self.isMod or self.isInsert:
                    BaseModal("Сохранить перед выходом?", self.handle_confirmation)
                else:
                    self.deleteItem()
            else:
                if self.isInsert:
                    await self.thisApi().delete(self.obj)
                dpg.hide_item(self.tab)

        async def handle_confirmation(self, result: bool):
            if self.isInsert:
                if not result:
                    await self.thisApi().delete(self.obj)
                else:
                    await self.saveForm()
            else:
                if result:
                    await self.saveForm()
            dpg.hide_item(self.tab)

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
                if getattr(self, f'idItem', None) is None:
                    obj = await self.thisApi().insert()
                    setattr(self, f'idItem', obj.id)
                    return obj
                return await self.thisApi().load(getattr(self, f'idItem', None))
            return self.obj
        
        def checwork(self):
            super().checwork()
            self.selection.oper("saveForm").isDisabled = not self.isMod
            self.selection.oper('returnResult').isVisible = self.isModal

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