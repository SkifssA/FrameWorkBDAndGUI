import inspect
import flet as ft

from .AbstractForm import AbstractForm
from ..package import Core_FileManagerPkg, asyncRun
from core.Core_Store import store

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

    async def open(self):
        self.page = store.page
        self.meta = await Core_FileManagerPkg.getMeta(self.get_impl_path())
        self.createMainForm()
