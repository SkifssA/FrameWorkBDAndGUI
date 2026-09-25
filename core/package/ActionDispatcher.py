import importlib
import inspect

from core.package.AsynRun import asyncRun

class ActionDispatcherPkg:
    def __init__(self, IsRaise:bool=True):
        self.IsRaise = IsRaise


    def action(self, sAction:str, kattr:dict={}, classMethod:bool=False):
        sNameClass, sNameMetod = sAction.split('.')
        sNameModule = f'module.{sNameClass[:sNameClass.find('_')].lower()}'
        try:
            module = importlib.import_module(sNameModule)
            if not hasattr(module, sNameClass):
                if self.IsRaise:
                    raise AttributeError(f"Класс {sNameClass} не найден в модуле {sNameModule}")
                
            cls =  getattr(module, sNameClass)
            if not hasattr(cls, sNameMetod):
                if self.IsRaise:
                    raise AttributeError(f"Метод {sNameMetod} не найден в классе {sNameClass}")
            
            attr = self._getMethod(cls, sNameMetod, classMethod)
            return self._runMethod(attr, kattr)
        except ImportError as e:
            # Раньше при IsRaise=False ошибка молча съедалась и action()
            # возвращал None; теперь хотя бы логируем.
            import logging
            logging.getLogger('NecoTab').error("Не удалось импортировать %s: %s", sNameModule, e)
            if self.IsRaise:
                raise ValueError(f"Не удалось импортировать модуль {sNameModule}: {e}") from e
        
    def _getMethod(self, cls, sNameMetod:str, classMethod:bool=False):
        """Получение метода класса"""
        if not classMethod:
            return getattr(cls(), sNameMetod)
        return getattr(cls, sNameMetod)
    
    def _runMethod(self, attr, kattr:dict={}):
        '''Выполнение метода класса'''
        if inspect.iscoroutinefunction(attr):
            # Это async def метод → вызываем и ждём
            return asyncRun(attr(**kattr))
        elif callable(attr):
            # Обычный метод
            return attr(**kattr)
        raise TypeError(f"Атрибут не является вызываемым: {attr!r}")
        
