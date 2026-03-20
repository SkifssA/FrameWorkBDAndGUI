from core.package import ASQL
from .FormFlet import BaseForm
from core.package.Core_AsynRunPkg import asyncRun
from core.Core_Store import store
import flet as ft
import flet_datatable2 as fdt


class EmptyList(BaseForm):            
    def _getCollumn(self)->dict[tuple[str]]:
        '''Получение столбцов'''
        attrs:dict = self.meta['attr']
        headRes = {col: (attrs[col]['caption'], attrs[col]['isVisible'], attrs[col]['edit']) for col in dict(sorted(attrs.items(), key=lambda x: x[1].get('order', 0)))}
        return headRes
    
    async def __getDataTab(self):
        '''Получение данных из БД для данной таблицы'''
        return await ASQL(*self.getSqlAndParam(await self.onRefresh()))
    
    def _getAttr(self, nameAttr:str):
        return self.selectRow.data[nameAttr]

    def _refresh(self, isUpdate:bool=False):
        row = []
        for i in asyncRun(self.__getDataTab()):
            row.append(ft.DataRow(
                cells=[ft.DataCell(ft.Text(i[key])) for key, item in self._getCollumn().items() if item[1]]
                ,data=i
                ,on_select_change=self.tabRow
            ))
        self.mainForm.rows = row
        if (len(row) > 0):
            self.__updageSelectRow(row[0])
        if isUpdate: store.page.update()

    def createMainForm(self):
        column = [ft.DataColumn(label=ft.Text(i[1][0]), visible=i[1][1]) for i in self._getCollumn().items()]

        q = fdt.DataTable2(columns=column, expand=True)
        return q
    
    def __updageSelectRow(self, control):
        for i in self.mainForm.rows:
            if i != control:
                i.color = None
            else:
                i.color = ft.Colors.INVERSE_PRIMARY
                self.selectRow = i

    def tabRow(self, e):
        self.__updageSelectRow(e.control)
        self.refreshChildren()

        store.page.update()