from abc import ABC, abstractmethod
import inspect

class AnyForm(ABC): 
    @abstractmethod
    def createMainForm(self, par)->int|str: pass

    @abstractmethod
    def validateClass(self): pass

    def openCh(self):
        '''Открытие дочерних форм.'''
        yield

    def _getAttr(self):pass
    def _refresh(self):pass
    def getAttr(self):pass
    def onRefresh(self):pass
    def onRefreshExt(self):pass
    def thisApi(self):pass

    def get_impl_path(self):
        """Путь к файлу, где определён класс"""
        file = inspect.getfile(self.__class__)
        w = file.find('modules')
        file = file[w:-3].replace('object', 'schemas')
        return file