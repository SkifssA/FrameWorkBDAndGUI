import dearpygui.dearpygui as dpg
import importlib

from ..package import ASQL

class BaseAvi:
    class DefaultList:
        async def open(self):
            with dpg.window(label="Таблица данных",
                            no_title_bar=True,        # убираем заголовок (опционально)
                            no_move=True,             # нельзя двигать
                            no_resize=True,           # нельзя менять размер
                            no_collapse=True,         # нельзя свернуть
                            width=-1,                 # ← растянуть по ширине
                            height=-1):
                # Создаём таблицу
                with dpg.theme() as table_theme:
                        with dpg.theme_component(dpg.mvTable):
                            dpg.add_theme_color(dpg.mvThemeCol_HeaderActive, (0, 0, 0, 0), category=dpg.mvThemeCat_Core)
                            dpg.add_theme_color(dpg.mvThemeCol_Header, (0, 0, 0, 0), category=dpg.mvThemeCat_Core)

                def clb_selectable(sender, app_data, user_data):
                    print(f"Row {user_data}")

                with dpg.table(header_row=True, # ← растягивает колонки
                                borders_innerH=True,
                                borders_innerV=True,
                                borders_outerH=True,
                                borders_outerV=True) as table_sel_rows:
                    data = await self.__getDataTab()
                    for i in data['column']:
                        dpg.add_table_column(label=i[1], user_data=i[0], enabled=(i[0] in self.showAttr))

                    for i in data['row']:
                        with dpg.table_row():
                            for j in i:
                                dpg.add_selectable(label=i[j], span_columns=True, callback=clb_selectable, user_data=i)
                dpg.bind_item_theme(table_sel_rows, table_theme)

        async def _getCollumn(self, column)->tuple[tuple[str]]:
            def getNameNotHL(name):
                return name[:-2] if name.endswith('HL') else name

            head = await (await self.thisApi()).getCaptionAttrClass()
            caption_map = {item['sCode']: item['sCaption'] for item in head}
            headRes = tuple((col, caption_map[getNameNotHL(col)] if getNameNotHL(col) in caption_map else col) for col in column)
            return headRes
        
        async def __getDataTab(self):
            res = {}
            res['row'] = await ASQL(await self.onRefresh())
            if res['row']:
                res['column'] = await self._getCollumn(res['row'][0].keys())
            else:
                res['column'] = await self._getCollumn(self.showAttr)
            return res

        def thisApi(self):
            outer_class_name = self.__class__.__qualname__.rsplit('.', 1)[0]
            # Получаем имя модуля, где определён класс
            module_name = self.__class__.__module__
            module = importlib.import_module(module_name)
            outer_class = getattr(module, outer_class_name)

            return outer_class.thisApi()

    class DefaultLookUp:
        pass