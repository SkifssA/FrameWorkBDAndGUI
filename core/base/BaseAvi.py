import dearpygui.dearpygui as dpg
import importlib

from ..package import ASQL
from ..empty.BaseForm import BaseForm
from ..empty.EmptyList import EmptyList
from ..empty.EmptyCard import EmptyCard
from .BaseOper import SetOper
from .BaseModal import DialogModal

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
            w = name.split('$', maxsplit=1)
            n, p = w[0], '$'.join(w[1:])
            if n == 'super':
                if self.parent != 'tab_bar':
                    w:BaseForm = dpg.get_item_user_data(self.parentTable)
                    return w.getAttr(p)  
            elif n == 'filter':
                return self.filter._getAttr(p)                           
            else:
                return self._getAttr(name)

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
      
        
        @SetOper(label='Обновить', order=1, img='2')
        async def refreshForm(self): await self.refresh()

    class DefaultList(DefaultDefault, EmptyList):
        
        @SetOper(label='Открыть', order=2, img='4')
        async def openForm(self): await self._getAvi().card(idItem=self.getAttr('id')).open()
        
        @SetOper(label='Создать', order=10, img='0')
        async def insert(self): await self._getAvi().card(isInsert=True).open()

        @SetOper(label='Удалить', order=20, img='3')
        async def delete(self):
            await self.thisApi()._deleteById(self.getAttr('id'))
            await self.refresh()

        @SetOper(label='Закрыть', order=10000, img='1')
        async def closeForm(self): dpg.delete_item(self.tab)


        def checwork(self):
            super().checwork()
            self.selection.oper(['openForm', 'delete']).isDisabled = self.getAttr('id') is None
            self.selection.oper('returnResult').isVisible = self.isModal

    class DefaultCard(DefaultDefault, EmptyCard): 
        @SetOper(label='Выбрать', order=-1, isVisible=False, img='10')
        async def returnResult(self):
            d = {}
            for i in self.returnAttr:
                d[i] = self.getAttr(i) 
            await self.callback(**d)
            self.closeForm()


        @SetOper(label='Закрыть', order=10000, img='1')
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

        @SetOper(label='Сохранить', order=1, img='5')
        async def saveForm(self):
            await self.thisApi().update(self.obj)
            self.isInsert = False
            self.isMod = False

        @SetOper(label='Обновить', order=-1, img='2')
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
        
        def _refresh(self):pass

        def _getAttr(self):pass

        def onRefreshExt(self):pass

        def createMainForm(self, par):pass