import inspect
import flet as ft
import re
import importlib

from .AbstractForm import AbstractForm
from ..package import Core_FileManagerPkg, asyncRun
from core.Core_Store import store
from core.empty.TabsFlet import Tabs

class BaseForm(AbstractForm): 
    def get_impl_path(self):
        """Путь к файлу, где определён класс"""
        file = inspect.getfile(self.__class__)
        w = file.find('modules')
        file = file[w:-3].replace('object', 'schemas')
        return file
    
    async def validateClass(self): pass

    def appendAction(self, obj, name):
        '''Создание обработчиков для операций'''
        bound_method = getattr(self, name)
        if obj._is_long:
            # return lambda: LoadModal(bound_method, f'Выполнение задачи \'{obj._oper_label}\'').show()
            pass
        else:
            return lambda: asyncRun(bound_method())

    async def open(self, parent:Tabs=None):
        self.page = store.page
        self.parentTabs = parent
        self.meta = await Core_FileManagerPkg.getMeta(self.get_impl_path(), self)
        self.mainForm = self.createMainForm()
        c = ft.Column(
            controls=[
                self.addTools() if parent is not None else ft.Row()
                ,self.mainForm   
            ]
        )
        if (parent is None):
            store.page.add(c)
        else:
            parent.add(ft.Tab(label=ft.Text(self.meta['caption']), data={'name':self.__getNameClass()}), c)
        store.page.update()

    def close(self):
        self.parentTabs.popByName(self.__getNameClass())

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
                objPath=i[-1].img,
                label=i[-1]._oper_label, 
                callback=self.appendAction(i[-1], i[0]),
                show=oper[i[0]]['isVisible'] if i[0] in oper else i[-1].isVisible
            ))
        return ft.Row(
            controls=b
            )

    def addButton(self, objPath, label, callback, show): 
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