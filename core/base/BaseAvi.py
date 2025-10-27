import dearpygui.dearpygui as dpg
import importlib

from ..empty.EmptyList import EmptyList
from .BaseOper import SetOper

class BaseAvi:
    class DefaultList(EmptyList):

        @SetOper(label='Закрыть')
        async def closeForm(self):
            dpg.hide_item(await (await self.thisApi())._getNameClass())

        def thisApi(self):
            outer_class_name = self.__class__.__qualname__.rsplit('.', 1)[0]
            # Получаем имя модуля, где определён класс
            module_name = self.__class__.__module__
            module = importlib.import_module(module_name)
            outer_class = getattr(module, outer_class_name)
            return outer_class.thisApi()

    class DefaultLookUp:
        pass