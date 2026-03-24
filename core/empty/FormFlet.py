import inspect
import flet as ft
import re
import importlib

from .AbstractForm import AnyForm
from ..package import Core_FileManagerPkg, asyncRun
from core.Core_Store import store
from core.empty.TabsFlet import Tabs
from core.empty.ColumnFlet import Column

class BaseForm(AnyForm):     
    async def validateClass(self): pass

    def appendAction(self, obj, name):
        '''Создание обработчиков для операций'''
        bound_method = getattr(self, name)
        if obj._is_long:
            # return lambda: LoadModal(bound_method, f'Выполнение задачи \'{obj._oper_label}\'').show()
            pass
        else:
            return lambda: asyncRun(bound_method())

    async def open(self, parent:Tabs|ft.Column=None, isUpdate:bool=True):
        self.parentTabs = parent
        self.meta = await Core_FileManagerPkg.getMeta(self.get_impl_path(), self)
        self.createForm()
        self.atrefCreateForm()
        self.createChildren()
        if isUpdate: store.page.update()

    def close(self):
        self.parentTabs.popByName(self.__getNameClass())

    def createTabs(self):
        t = Tabs(
                data=self,
                length=1,
                expand=True,
                content=ft.Column(
                    expand=True,
                    controls=[
                        tab_bar := ft.TabBar(
                            tabs=[]
                        ),
                        tab_view := ft.TabBarView(
                            expand=True,
                            controls=[],
                        ),
                    ],
                ),
                visible= False
            )
        t.init2(tab_bar, tab_view)
        return t

    def createForm(self):
        self.mainForm = self.createMainForm()
        tabs = self.createTabs()
        mainCont = ft.Column(
            expand=True
            ,controls=[
                self.addTools() if self.parentTabs is not None else ft.Row()
                ,self.mainForm   
                ,tabs
            ]
        )
        self.mainConts = ft.Row(
            expand=True
            ,controls=[
                leftCont:=Column(expand=True, visible=False, data=self)
                ,mainCont
                ,rightCont:=Column(expand=True, visible=False, data=self)
            ]
        )
        self.locationsChildrens = {
            'bottom': tabs 
            ,'left': leftCont
            ,'right': rightCont
        }
        if (self.parentTabs is None):
            store.page.add(self.mainConts)
        elif type(self.parentTabs) == Tabs:
            self.parentTabs.add(ft.Tab(label=ft.Text(self.meta['caption']), data={'name':self.__getNameClass()}), self.mainConts)
        elif type(self.parentTabs) == Column:
            self.parentTabs.add(self.mainConts)

    def addTools(self):
        '''Обработка и создание операций'''
        q = []
        for name, obj in inspect.getmembers(self.__class__, predicate=inspect.isfunction):
            if hasattr(obj, '_is_oper_handler'):
                q.append((name, obj))
            
        oper = self.meta.get('oper', {})
        b = []
        for i in sorted(q, key=lambda x: x[-1]._order):
            b.append(self.addButton(
                label=i[-1]._oper_label, 
                callback=self.appendAction(i[-1], i[0]),
                show=oper[i[0]]['isVisible'] if i[0] in oper else i[-1].isVisible
            ))
        return ft.Row(
            controls=b
            )

    def addButton(self, label, callback, show): 
        return ft.ElevatedButton(label, on_click=callback, visible=show)

    def getSqlAndParam(self, sql:str)->tuple[str, list]:
        par = [self.getAttr(i) for i in re.findall(r':([^ ]*)', sql)]
        sql = re.sub(r':[^ ]*', '?', sql)
        return (sql, par)

    def __getNameClass(self):
        return f'{self.__class__.__qualname__.rsplit('.', 1)[0]}#{self.__class__.__name__}'

    def _getAvi(self):
            outer_class_name = self.__class__.__qualname__.rsplit('.', 1)[0]
            # Получаем имя модуля, где определён класс
            module_name = self.__class__.__module__
            module = importlib.import_module(module_name)
            return getattr(module, outer_class_name)
    
    def createChildren(self):
        from core.formhandle.FornManeger import FormHandle
        self.childrens:tuple[FormHandle] = tuple(self.openCh())
        for i in self.childrens:
            if i is not None:
                i.param(parent=self, isUpdate=False).open()

    def openCh(self):
        '''Открытие дочерних форм.'''
        yield

    def refresh(self):
        self._refresh()
        self.refreshChildren()
        
    def refreshChildren(self):
        for i in self.childrens:
            if i is not None:
                i.clsForm.refresh()

    def atrefCreateForm(self):
        self._refresh()