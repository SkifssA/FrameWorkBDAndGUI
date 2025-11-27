import dearpygui.dearpygui as dpg
from ..package import ASQL

import asyncio
import re

from .BaseForm import BaseForm

class EmptyList(BaseForm):
    def createTheme(self):
        '''Создание темы'''
        with dpg.theme() as table_theme:
            with dpg.theme_component(dpg.mvTable):
                dpg.add_theme_color(dpg.mvThemeCol_HeaderActive, (0, 0, 0, 0), category=dpg.mvThemeCat_Core)
                dpg.add_theme_color(dpg.mvThemeCol_Header, (0, 0, 0, 0), category=dpg.mvThemeCat_Core)
        return table_theme
                
    async def _refresh(self):
        '''Обнолвение формы'''
        data = await self.__getDataTab()
        s = True
        tabl = self.mainForm
        if dpg.does_item_exist(tabl):
            children = dpg.get_item_children(tabl, slot=1) + dpg.get_item_children(tabl, slot=0) # slot=0 — основной контейнер
            for child in children:
                dpg.delete_item(child)

            oneRow = None

            for i in data['column']:
                    dpg.add_table_column(label=i[1], user_data=i[0], enabled=(i[0] in self.showAttr), parent=tabl)
            for row in data['row']:
                with dpg.table_row(parent=tabl):
                    for j in row:
                        q = dpg.add_selectable(label=row[j], span_columns=True, user_data=row, callback=lambda x, y, z: self._click(x, tabl))
                        if s:
                            s=False
                            oneRow = q
            if oneRow is not None:
                self._click(oneRow, tabl)

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
        '''Обновление. Пользовательское'''
        await self._refresh()
        await self.refreshCh()

    def _click(self, tagSelf, tagTable):
        '''Обработчик выбора строки в таблице'''
        self._oneShow(tagSelf, tagTable)
        self.checwork()

    def checwork(self):
        '''Операция выполняемая при выборе строки'''
        try:
            asyncio.get_running_loop()
            asyncio.create_task(self.refreshCh())
        except:
            asyncio.run(self.refreshCh())

    def _oneShow(self, tagSelf, tagTable):
        '''Отвечает только за единичный выбор строки в таблице'''
        for i in dpg.get_item_children(tagTable, slot=1):
            ch = dpg.get_item_children(i, slot=1)
            for j in ch:
                dpg.set_value(j, tagSelf in ch)

    async def _getCollumn(self, column)->tuple[tuple[str]]:
        '''Получение столбцов'''
        def getNameNotHL(name):
            return name[:-2] if name.endswith('HL') else name

        head = await self.thisApi().getCaptionAttrClass()
        caption_map = {item['sCode']: item['sCaption'] for item in head}
        headRes = tuple((col, caption_map[getNameNotHL(col)] if getNameNotHL(col) in caption_map else col) for col in column)
        return headRes
    
    async def __getDataTab(self, column=True):
        '''Получение данных из БД для данной таблицы'''
        res = {}
        res['row'] = await ASQL(await self.onRefresh())
        if column:
            if res['row']:
                res['column'] = await self._getCollumn(res['row'][0].keys())
            else:
                res['column'] = await self._getCollumn(self.showAttr)
        return res

    def createMainForm(self, par):
        return dpg.add_table(header_row=True,
                        height=-1,
                        borders_innerH=True,
                        borders_innerV=True,
                        borders_outerH=True,
                        borders_outerV=True,
                        parent=par,
                        scrollY=True)
        
    