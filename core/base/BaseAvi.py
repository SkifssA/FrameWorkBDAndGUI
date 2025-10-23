import dearpygui.dearpygui as dpg
import importlib

from ..package import ASQL

class BaseAvi:
    class DefaultList:
        async def open(self):
                data = await self.__getDataTab()
                sTag = await (await self.thisApi())._getNameClass()
                if dpg.does_item_exist(sTag):
                    dpg.show_item(sTag)
                else:
                    self.createTable(sTag, data['column'])

                await self._refresh(sTag, data['row'])
                dpg.set_value("tab_bar", sTag)

        def createTheme(self):
            with dpg.theme() as table_theme:
                with dpg.theme_component(dpg.mvTable):
                    dpg.add_theme_color(dpg.mvThemeCol_HeaderActive, (0, 0, 0, 0), category=dpg.mvThemeCat_Core)
                    dpg.add_theme_color(dpg.mvThemeCol_Header, (0, 0, 0, 0), category=dpg.mvThemeCat_Core)
                    return table_theme

        async def _refresh(self, tabl, rows):
            tabl += self.__class__.__name__
            children = dpg.get_item_children(tabl, slot=1)  # slot=0 — основной контейнер
            for child in children:
                if dpg.get_item_type(child) == "mvAppItemType::mvTableRow":
                    dpg.delete_item(child)

            for i in rows:
                with dpg.table_row(parent=tabl):
                    for j in i:
                        dpg.add_selectable(label=i[j], span_columns=True, user_data=i)

        async def _getCollumn(self, column)->tuple[tuple[str]]:
            def getNameNotHL(name):
                return name[:-2] if name.endswith('HL') else name

            head = await (await self.thisApi()).getCaptionAttrClass()
            caption_map = {item['sCode']: item['sCaption'] for item in head}
            headRes = tuple((col, caption_map[getNameNotHL(col)] if getNameNotHL(col) in caption_map else col) for col in column)
            return headRes
        
        async def __getDataTab(self, column=True):
            res = {}
            res['row'] = await ASQL(await self.onRefresh())
            if column:
                if res['row']:
                    res['column'] = await self._getCollumn(res['row'][0].keys())
                else:
                    res['column'] = await self._getCollumn(self.showAttr)
            return res

        def createTable(self, tabl, collumn):
            tab = dpg.add_tab(tag=tabl, label=tabl, parent='tab_bar')

            dpg.add_button(label="Закрыть", callback=lambda: dpg.hide_item(tab), parent=tab)

            with dpg.table(header_row=True, # ← растягивает колонки
                            borders_innerH=True,
                            borders_innerV=True,
                            borders_outerH=True,
                            borders_outerV=True,
                            parent=tab,
                            tag=tabl+self.__class__.__name__) as table_sel_rows:
                for i in collumn:
                    dpg.add_table_column(label=i[1], user_data=i[0], enabled=(i[0] in self.showAttr))
            dpg.bind_item_theme(table_sel_rows, self.createTheme())

        def thisApi(self):
            outer_class_name = self.__class__.__qualname__.rsplit('.', 1)[0]
            # Получаем имя модуля, где определён класс
            module_name = self.__class__.__module__
            module = importlib.import_module(module_name)
            outer_class = getattr(module, outer_class_name)

            return outer_class.thisApi()

    class DefaultLookUp:
        pass