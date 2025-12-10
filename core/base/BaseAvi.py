import dearpygui.dearpygui as dpg
import importlib

from ..package import ASQL, Core_ActionDispatcherPkg
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

    class DefaultDefault():
        def getAttr(self, name:str):
            if name.split('$', maxsplit=1)[0] == 'super':
                if self.parent != 'tab_bar':
                    w = self.get_any_row(self.parentTable)
                    if w is not None and w != {}:
                        return w[name.split('$')[-1]]     
                    else:
                        return None                           
            else:
                row = self.get_row()
                if name in row:
                    return row[name]
            return None

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

        def get_row(self):
            return self.get_any_row(self.mainForm)
    
        def get_any_row(self, tagTable):
            if not dpg.does_item_exist(tagTable):
                return {}
            for i in dpg.get_item_children(tagTable, slot=1):
                for j in dpg.get_item_children(i, slot=1):
                    if dpg.get_value(j):
                        return dpg.get_item_user_data(j)
      
    class DefaultList(DefaultDefault, EmptyList):

        @SetOper(label='Обновить', order=1)
        async def refreshForm(self):
            await self.refresh()

        @SetOper(label='Открыть', order=2)
        async def openForm(self):
            await self._getAvi().card(idItem=self.getAttr('id')).open()
        
        @SetOper(label='Создать', order=10)
        async def insert(self):
            await self._getAvi().card().open()

        @SetOper(label='Закрыть', order=10000)
        async def closeForm(self):
            dpg.hide_item(self.tab)

    class DefaultCard(DefaultDefault, EmptyCard): 
        @SetOper(label='Закрыть', order=10000)
        async def closeForm(self):
            if self.mod:
                BaseModal("Сохранить перед выходом?", self.handle_confirmation)
            else:
                dpg.hide_item(self.tab)

        async def handle_confirmation(self, result: bool):
            if result:
                await self.saveForm()
            dpg.hide_item(self.tab)

        @SetOper(label='Сохранить', order=1)
        async def saveForm(self):
            await self.thisApi().update(self.obj)
            self.mod = False

        async def initInput(self):
            data = self.thisApi()._getDataRop(self.obj)

            """Костыть для проверки"""
            data['idConfigHL'] = None
            data['idConfigLookHL'] = 3

            for i in self.tagInput:
                dpg.configure_item(self.tagInput[i], callback=getattr(self, f'set{i}', None))
                typeW = dpg.get_item_type(self.tagInput[i])
                if typeW == "mvAppItemType::mvCombo":
                    await self._initLookUp(i, data[i])
                elif typeW == "mvAppItemType::mvCheckbox":
                    await self._initCheck(i, data[i])
                else:
                    await self._initAll(i, data[i])

        def afterSetter(self):
            self.mod = True

        async def getObj(self):
            if getattr(self, f'idItem', None) is None:
                return await self.thisApi().insert()
            return await self.thisApi().load(getattr(self, f'idItem', None))

        async def afterCreate(self):
            self.obj = await self.getObj()
            await self.initInput()

        async def _initLookUp(self, i, defValue):
            dpg.configure_item(self.tagInput[i], default_value=defValue if defValue is not None else '')
            nameClass = self.meta['attr'][i]['refTab']
            nameLook = self.meta['attr'][i]['display']
            look = await Core_ActionDispatcherPkg().action(f"{nameClass}Avi.{nameLook}")
            data = await look.getData()
            dataLook = list(i['sHeadLine'] for i in data)
            dpg.configure_item(self.tagInput[i], items=dataLook)
            dpg.configure_item(self.tagInput[i], user_data=look)

        async def _initCheck(self, i, defValue):
            dpg.configure_item(self.tagInput[i], default_value=bool(defValue) if defValue is not None else False)

        async def _initAll(self, i, defValue):
            dpg.configure_item(self.tagInput[i], default_value=defValue if defValue is not None else '')

    class DefaultDet(DefaultDefault, EmptyList):
        def getIdMaster(self):
            return self.getAttr('super$id')

    class DefaultLookUp: 
        async def getData(self):
            self.data = await ASQL(await self.onRefresh())
            return self.data
        
        def getId(self, value:str)->int:
            return tuple(i['id'] for i in self.data if i['sHeadLine'] == value)[0]