import dearpygui.dearpygui as dpg
from ..package import ASQL
import inspect
import asyncio
import re

class EmptyList:
    def getTag(self):
        return self.thisApi()._getNameClass() + str(self.parent)

    async def open(self, parent='tab_bar'):
        data = await self.__getDataTab()
        self.parent = parent
        self.sTag = self.getTag()
        if dpg.does_item_exist(self.sTag):
            dpg.show_item(self.sTag)
            await self._refresh(data)
            await self.refreshCh()
        else:
            master = await self.createTab(self.sTag, parent)
            await self._refresh(data)
            self.ch = tuple(self.openCh(master))
            for i in self.ch:
                print(f'{i=}')
                await i.open(master)

    async def refreshCh(self):
        for i in self.ch:
            await i.refresh()

    def openCh(self, master):
        return []

    def createTheme(self):
        with dpg.theme() as table_theme:
            with dpg.theme_component(dpg.mvTable):
                dpg.add_theme_color(dpg.mvThemeCol_HeaderActive, (0, 0, 0, 0), category=dpg.mvThemeCat_Core)
                dpg.add_theme_color(dpg.mvThemeCol_Header, (0, 0, 0, 0), category=dpg.mvThemeCat_Core)
        return table_theme
                
    async def _refresh(self, data):
        s = True
        tabl = self.sTag + self.__class__.__name__
        children = dpg.get_item_children(tabl, slot=1) + dpg.get_item_children(tabl, slot=0) # slot=0 — основной контейнер
        for child in children:
            dpg.delete_item(child)
        
        for i in data['column']:
                dpg.add_table_column(label=i[1], user_data=i[0], enabled=(i[0] in self.showAttr), parent=tabl)
        for row in data['row']:
            with dpg.table_row(parent=tabl):
                for j in row:
                    q = dpg.add_selectable(label=row[j], span_columns=True, user_data=row, callback=lambda x, y, z: self._click(x, tabl))
                    if s:
                        s=False
                        self._click(q, tabl)

    async def __getWhereSql(self):
            res = await self.onRefresh()
            param = []
            for i in self.flt:
                for j in re.findall(r':([^ ]*)', i):
                    param.append(self.getAttr(j))
            where = [re.sub(r':[^ ]*', '?', i) for i in self.flt]
            if self.flt != []:
                res += f'where {' and '.join(where)}'
            return [res, param if param != [] else None]

    async def refresh(self):
        data = await self.__getDataTab()
        self.sTag = self.thisApi()._getNameClass()
        await self._refresh(data)

    def _click(self, tagSelf, tagTable):
        self._oneShow(tagSelf, tagTable)
        self.checwork()

    def checwork(self):
        try:
            asyncio.get_running_loop()
            asyncio.create_task(self.refreshCh())
        except:
            asyncio.run(self.refreshCh())

    def _oneShow(self, tagSelf, tagTable):
        for i in dpg.get_item_children(tagTable, slot=1):
            ch = dpg.get_item_children(i, slot=1)
            for j in ch:
                dpg.set_value(j, tagSelf in ch)

    async def _getCollumn(self, column)->tuple[tuple[str]]:
        def getNameNotHL(name):
            return name[:-2] if name.endswith('HL') else name

        head = await self.thisApi().getCaptionAttrClass()
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

    async def createTab(self, tabl, parent='tab_bar'):
        tab = dpg.add_tab(tag=tabl, label=tabl, parent=parent)
        dpg.configure_item(parent, show=True)

        with dpg.group(parent=tab) as WWWW:
            pass

        return await self.createTable(WWWW)
       
    async def createTable(self, par):
        self.sTag = self.thisApi()._getNameClass()
        with dpg.group(horizontal=True, parent=par):
            await self.addTools()
        with dpg.table(header_row=True, # ← растягивает колонки
                        borders_innerH=True,
                        borders_innerV=True,
                        borders_outerH=True,
                        borders_outerV=True,
                        tag=self.sTag+self.__class__.__name__,
                        parent=par): pass
        with dpg.tab_bar(show=False, parent=par) as e: pass
        return e

    async def addTools(self):
        nameApi = self.getTag()
        q = []
        for name, obj in inspect.getmembers(self.__class__, predicate=inspect.isfunction):
            if hasattr(obj, '_is_oper_handler'):
                q.append((name, obj))
            
        for i in sorted(q, key=lambda x: x[-1]._order): 
            dpg.add_button(label=i[-1]._oper_label, callback=self.appendAction(i[-1], i[0]), tag=f"{nameApi}_{i[-1]._oper_id}")

    def appendAction(self, obj, name):
        bound_method = getattr(self, name)
        if obj._is_long:
            return self.__createRunning(bound_method)
        else:
            return lambda: asyncio.run(bound_method())