import dearpygui.dearpygui as dpg
from ..package import ASQL

import asyncio


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
                q = data['column'][i]
                dpg.add_table_column(label=q[0], user_data=i, enabled=q[1], parent=tabl)
            for row in data['row']:
                with dpg.table_row(parent=tabl):
                    w = True
                    for j in data['column']:
                        if data['column'][j][2] == 'check':
                            dpg.set_value(dpg.add_checkbox(enabled=False), bool(row[j]) if row[j] is not None else False)
                        else:
                            if w and data['column'][j][1]:
                                q = dpg.add_selectable(label=row[j], span_columns=True, user_data=row, callback=lambda x, y, z: self._click(x, tabl), height=21)
                                w = False
                                if s:
                                    s=False
                                    oneRow = q
                            else:
                                dpg.add_text(row[j] if row[j] is not None else "")
                        
            if oneRow is not None:
                self._oneShow(oneRow, tabl)
                self.tagRow = oneRow
            self.checwork()

    def _click(self, tagSelf, tagTable):
        '''Обработчик выбора строки в таблице'''
        self._oneShow(tagSelf, tagTable)
        self._checwork(tagSelf)

    def _checwork(self, tagRow:str):
        if tagRow != self.tagRow:
            self.tagRow = tagRow
            '''Операция выполняемая при выборе строки'''
            try:
                asyncio.get_running_loop()
                asyncio.create_task(self.refreshCh())
            except:
                asyncio.run(self.refreshCh())
            self.checwork()

    def _oneShow(self, tagSelf, tagTable):
        '''Отвечает только за единичный выбор строки в таблице'''
        for i in dpg.get_item_children(tagTable, slot=1):
            ch = dpg.get_item_children(i, slot=1)
            for j in ch:
                if dpg.get_item_type(j) == "mvAppItemType::mvSelectable":
                    dpg.set_value(j, tagSelf in ch)

    async def _getCollumn(self)->tuple[tuple[str]]:
        '''Получение столбцов'''
        attrs:dict = self.meta['attr']
        headRes = {col: (attrs[col]['caption'], attrs[col]['isVisible'], attrs[col]['edit']) for col in dict(sorted(attrs.items(), key=lambda x: x[1].get('order', 0)))}
        return headRes
    
    async def __getDataTab(self, column=True):
        '''Получение данных из БД для данной таблицы'''
        res = {}
        res['row'] = await ASQL(*self.getSqlAndParam(await self.onRefresh()))
        res['column'] = await self._getCollumn()
        return res

    def createMainForm(self, par):
        return dpg.add_table(header_row=True,
                             resizable=True,
                             height=-1,
                             borders_innerH=True,
                             borders_innerV=True,
                             borders_outerH=True,
                             borders_outerV=True,
                             parent=par,
                             scrollY=True)
    
    def _getAttr(self, nameAttr:str):
        row = self.get_row()
        if nameAttr in row:
            return row[nameAttr]
        return None

    def get_row(self):
        return self.get_any_row(self.mainForm)
    
    def get_any_row(self, tagTable)->dict:
        if not dpg.does_item_exist(tagTable):
            return {}
        for i in dpg.get_item_children(tagTable, slot=1):
            for j in dpg.get_item_children(i, slot=1):
                if dpg.get_value(j) and dpg.get_item_user_data(j):
                    return dpg.get_item_user_data(j)
        return {}
        
    