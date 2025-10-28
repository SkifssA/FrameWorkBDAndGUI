import dearpygui.dearpygui as dpg
from ..package import ASQL
import inspect
import asyncio

class EmptyList:
    async def open(self):
        data = await self.__getDataTab()
        sTag = await (await self.thisApi())._getNameClass()
        if dpg.does_item_exist(sTag):
            dpg.show_item(sTag)
        else:
            self.createTable(sTag, data['column'])

        await self._refresh(sTag, data)
        dpg.set_value("tab_bar", sTag)

    def createTheme(self):
        with dpg.theme() as table_theme:
            with dpg.theme_component(dpg.mvTable):
                dpg.add_theme_color(dpg.mvThemeCol_HeaderActive, (0, 0, 0, 0), category=dpg.mvThemeCat_Core)
                dpg.add_theme_color(dpg.mvThemeCol_Header, (0, 0, 0, 0), category=dpg.mvThemeCat_Core)
        return table_theme
                
    async def _refresh(self, tabl, data):
        tabl += self.__class__.__name__
        children = dpg.get_item_children(tabl, slot=1) + dpg.get_item_children(tabl, slot=0) # slot=0 — основной контейнер
        for child in children:
            dpg.delete_item(child)
        
        for i in data['column']:
                dpg.add_table_column(label=i[1], user_data=i[0], enabled=(i[0] in self.showAttr), parent=tabl)
        for row in data['row']:
            with dpg.table_row(parent=tabl):
                for j in row:
                    dpg.add_selectable(label=row[j], span_columns=True, user_data=row, callback=lambda x, y, z: self._click(x, tabl))

    async def refresh(self):
        data = await self.__getDataTab()
        sTag = await (await self.thisApi())._getNameClass()
        await self._refresh(sTag, data)

    def _click(self, tagSelf, tagTable):
        for i in dpg.get_item_children(tagTable, slot=1):
            ch = dpg.get_item_children(i, slot=1)
            for j in ch:
                dpg.set_value(j, tagSelf in ch)

    async def get_row(self):
        tagTable = (await (await self.thisApi())._getNameClass()) + self.__class__.__name__
        for i in dpg.get_item_children(tagTable, slot=1):
            for j in dpg.get_item_children(i, slot=1):
                if dpg.get_value(j):
                    return dpg.get_item_user_data(j)

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

        with dpg.group(horizontal=True, parent=tab):
            self.addTools()

        with dpg.table(header_row=True, # ← растягивает колонки
                        borders_innerH=True,
                        borders_innerV=True,
                        borders_outerH=True,
                        borders_outerV=True,
                        parent=tab,
                        tag=tabl+self.__class__.__name__) as table_sel_rows:
            pass
        # dpg.bind_item_theme(table_sel_rows, self.createTheme())

    def addTools(self):
        q = []
        for name, obj in inspect.getmembers(self.__class__, predicate=inspect.isfunction):
            if hasattr(obj, '_is_oper_handler'):
                q.append((name, obj))
            
        for i in sorted(q, key=lambda x: x[-1]._order):    
            dpg.add_button(label=i[-1]._oper_label, callback=self.appendAction(i[-1], i[0]))

    def appendAction(self, obj, name):
        bound_method = getattr(self, name)
        if obj._is_long:
            return self.__createRunning(bound_method)
        else:
            return lambda: asyncio.run(bound_method())