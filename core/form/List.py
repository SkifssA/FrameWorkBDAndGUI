import dearpygui.dearpygui as dpg

from core.package import ASQL
from core.form.Base import Base
from core.package.Core_AsynRunPkg import asyncRun

class List(Base):
    def __init__(self):
        super().__init__()
        self.column = None

    def createTheme(self):
        '''Создание темы'''
        with dpg.theme() as table_theme:
            with dpg.theme_component(dpg.mvTable):
                dpg.add_theme_color(dpg.mvThemeCol_HeaderActive, (0, 0, 0, 0), category=dpg.mvThemeCat_Core)
                dpg.add_theme_color(dpg.mvThemeCol_Header, (0, 0, 0, 0), category=dpg.mvThemeCat_Core)
        return table_theme
                
    async def _createColumn(self, tabl):
        '''Создание столбцов'''
        self.column = []
        self._getCollumn()
        for key, value in self.headRes.items():
            self.column.append(dpg.add_table_column(label=value[0]
                                                    , user_data=(key, value[2], value[1])
                                                    , enabled=value[1]
                                                    , parent=tabl))

    async def _refresh(self):
        '''Обнолвение формы'''
        rows = await self.__getDataTab()
        tabl = self.mainForm
        if dpg.does_item_exist(tabl):
            children = dpg.get_item_children(tabl, slot=1) # slot=0 — основной контейнер
            for child in children:
                dpg.delete_item(child)

            oneRow = None
            for row in rows:
                with dpg.table_row(parent=tabl):
                    w = True
                    for j in self.column:
                        tagCol, edit, isVis = dpg.get_item_user_data(j)
                        valueRow = row[tagCol]
                        if edit == 'check':
                            dpg.set_value(dpg.add_checkbox(enabled=False), bool(valueRow) if valueRow is not None else False)
                        elif w and isVis:
                            q = dpg.add_selectable(label=valueRow, span_columns=True, user_data=row, callback=lambda x, y, z: self._click(x, tabl), height=21)
                            w = False
                            if oneRow is None:
                                oneRow = q
                        else:
                            dpg.add_text(valueRow if valueRow is not None else "")
                        
            if oneRow is not None:
                self._oneShow(oneRow, tabl)
                self.tagRow = oneRow
            self.checwork()

    def _click(self, tagSelf, tagTable):
        '''Обработчик выбора строки в таблице'''
        self._oneShow(tagSelf, tagTable)
        self._checwork(tagSelf)

    def _checwork(self, tagRow:str):
        '''Операция выполняемая при выборе строки'''
        if tagRow != self.tagRow:
            self.tagRow = tagRow
            asyncRun(self.refreshCh())
            self.checwork()

    def _oneShow(self, tagSelf, tagTable):
        '''Отвечает только за единичный выбор строки в таблице'''
        for i in dpg.get_item_children(tagTable, slot=1):
            ch = dpg.get_item_children(i, slot=1)
            for j in ch:
                if dpg.get_item_type(j) == "mvAppItemType::mvSelectable":
                    dpg.set_value(j, tagSelf in ch)

    def _getCollumn(self)->dict[tuple[str]]:
        '''Получение столбцов'''
        attrs:dict = self.meta['attr']
        self.headRes = {col: (attrs[col]['caption'], attrs[col]['isVisible'], attrs[col]['edit']) for col in dict(sorted(attrs.items(), key=lambda x: x[1].get('order', 0)))}
        returnSelect = asyncRun(ASQL(*self.getSqlAndParam(self.onRefresh() + '\nLimit 0')))[0]
        for i in returnSelect.keys():
            if not i in self.headRes.keys():
                self.headRes[i] = (i, True, 'edit')
    
    async def __getDataTab(self):
        '''Получение данных из БД для данной таблицы'''
        return await ASQL(*self.getSqlAndParam(self.onRefresh()))
    
    def createMainForm(self, par):
        w = dpg.add_table(header_row=True,
                             resizable=True,
                             height=-1,
                             borders_innerH=True,
                             borders_innerV=True,
                             borders_outerH=True,
                             borders_outerV=True,
                             parent=par,
                             scrollY=True
                            )
        return w
    
    async def afterCreate(self):
        await self._createColumn(self.mainForm)

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
        
    