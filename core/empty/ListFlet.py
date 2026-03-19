from ..package import ASQL
from .FormFlet import BaseForm
from core.empty.TabsFlet import Tabs
from core.package.Core_AsynRunPkg import asyncRun
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

    async def _refresh(self):pass

    def createMainForm(self):
        self.column = [ft.DataColumn(label=ft.Text(i[1][0]), visible=i[1][1]) for i in self._getCollumn().items()]
        q = ft.Column(
            controls=[
                tabl:=ft.DataTable(
                    expand=True,
                    columns= self.column)
            ],
            scroll=ft.ScrollMode.ADAPTIVE,
            )
        
        self.tabl=tabl
        self.refresh()
        return q
    
    def __updageSelectRow(self, control):
        for i in self.tabl.rows:
            if i != control:
                i.color = None
            else:
                i.color = ft.Colors.DEEP_ORANGE_300
                self.selectRow = i

    def refresh(self):
        self.row = []
        for i in asyncRun(self.__getDataTab()):
            self.row.append(ft.DataRow(
                cells=[ft.DataCell(ft.Text(i[key])) for key, item in self._getCollumn().items() if item[1]]
                ,data=i
                ,on_select_change=self.tabRow
            ))
        self.tabl.rows = self.row

    def tabRow(self, e):
        self.__updageSelectRow(e.control)
        self.page.update()