import dearpygui.dearpygui as dpg
import importlib
import asyncio

from ..empty.EmptyList import EmptyList
from .BaseOper import SetOper

class BaseAvi:
    class DefaultDefault():
        def getAttr(self, name:str):
            if name.split('$', maxsplit=1)[0] == 'super':
                if self.parent != 'tab_bar':
                    master = dpg.get_item_parent(self.parent)
                    for i in dpg.get_item_children(master, slot=1):
                        if dpg.get_item_type(i) == 'mvAppItemType::mvTable':
                            return self.get_any_row(i)[name.split('$')[-1]]
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
            tagTable = self.thisApi()._getNameClass() + self.__class__.__name__
            return self.get_any_row(tagTable)
    
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
            dpg.hide_item(self.getTag())

    class DefaultDet(DefaultDefault, EmptyList):
        def getIdMaster(self):
            return self.getAttr('super$id')

    class DefaultLookUp:
        pass