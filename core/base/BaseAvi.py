import dearpygui.dearpygui as dpg
import importlib
import asyncio
from ..package import ASQL, Core_ActionDispatcherPkg

from ..empty.EmptyList import EmptyList
from ..empty.EmptyCard import EmptyCard
from .BaseOper import SetOper

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
            outer_class_name = self.__class__.__qualname__.rsplit('.', 1)[0]
            # Получаем имя модуля, где определён класс
            module_name = self.__class__.__module__
            module = importlib.import_module(module_name)
            outer_class = getattr(module, outer_class_name)
            return outer_class.thisApi()
        
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
        @SetOper(label='Закрыть', order=10000)
        async def closeForm(self):
            dpg.hide_item(self.tab)

    class DefaultCard(DefaultDefault, EmptyCard): 

        @SetOper(label='Закрыть', order=10000)
        async def closeForm(self):
            dpg.hide_item(self.tab)

        @SetOper(label='Сохранить', order=1)
        async def saveForm(self):
            dpg.hide_item(self.tab)

        async def initInput(self):
            for i in self.tagInput:
                if dpg.get_item_type(self.tagInput[i]) == "mvAppItemType::mvCombo":
                    nameClass = self.meta['attr'][i]['refTab']
                    nameLook = self.meta['attr'][i]['display']
                    look = await Core_ActionDispatcherPkg().action(f"{nameClass}Avi.{nameLook}")
                    data = await look.getData()
                    dataLook = list(i['sHeadLine'] for i in data)
                    dpg.configure_item(self.tagInput[i], items=dataLook)
                    dpg.configure_item(self.tagInput[i], user_data=look)
                    dpg.configure_item(self.tagInput[i], callback=self.w)

        def w(self, sender, app_data, user_data):
            idLook = user_data.getId(app_data)
            print(f'{idLook=}')

        async def afterCreate(self):
            await self.initInput()

    class DefaultDet(DefaultDefault, EmptyList):
        def getIdMaster(self):
            return self.getAttr('super$id')

    class DefaultLookUp: 
        async def getData(self):
            self.data = await ASQL(await self.onRefresh())
            return self.data
        
        def getId(self, value:str)->int:
            return tuple(i['id'] for i in self.data if i['sHeadLine'] == value)[0]