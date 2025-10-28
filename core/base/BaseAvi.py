import dearpygui.dearpygui as dpg
import importlib
import asyncio

from ..empty.EmptyList import EmptyList
from .BaseOper import SetOper

class BaseAvi:
    class DefaultList(EmptyList):

        @SetOper(label='Закрыть', order=10000)
        async def closeForm(self):
            dpg.hide_item(await (await self.thisApi())._getNameClass())

        def getAttr(self, name):
            row = asyncio.run(self.get_row())
            if name in row:
                return row[name]
            return None

        async def thisRop(self):
            row = await self.get_row()
            return await (await self.thisApi())._createRop(row)

        def thisApi(self):
            outer_class_name = self.__class__.__qualname__.rsplit('.', 1)[0]
            # Получаем имя модуля, где определён класс
            module_name = self.__class__.__module__
            module = importlib.import_module(module_name)
            outer_class = getattr(module, outer_class_name)
            return outer_class.thisApi()

    class DefaultLookUp:
        pass