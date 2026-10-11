import importlib
import inspect

from core.package.AsynRun import asyncRun
from core.package.FileManager import FileManagerPkg

def getModule(nameClass: str)->str:
    return nameClass[:nameClass.find('_')].lower()

class ModuleManagerPkg:
    _PATH_APP_CONFIG = "module/{module}/config/app.json"
    _PATH_HOOKS = "module/{module}/config/hooks.json"
    _PATH_PROJECT = "project.yaml"

    def __init__(self):
        self.cacheHooks = {}

    def _parseAction(self, sAction:str)->tuple[str, str]:
        sNameClass, x, sNameMetod = sAction.partition('.')

        if sNameMetod == '' or sNameClass == '' or sNameMetod.find('.') != -1:
            raise AttributeError(f"Не верные данные для \'sAction\'")

        if sNameMetod.startswith('_'):
            raise AttributeError(f"Можно вызывать методы без _")
            
        return sNameClass, sNameMetod

    def _action(self, sAction:str, kattr:dict={}, classMethod:bool=False):
        sNameClass, sNameMetod = self._parseAction(sAction)
        sNameModule = f'module.{getModule(sNameClass)}'
        try:
            cls = self._getClass(sNameClass)
            if not hasattr(cls, sNameMetod):
                raise AttributeError(f"Метод {sNameMetod} не найден в классе {sNameClass}")
            
            attr = self._getMethod(cls, sNameMetod, classMethod)
            return self._runMethod(attr, kattr)
        except ImportError as e:
                raise ValueError(f"Не удалось импортировать модуль {sNameModule}: {e}")

    def action(self, sAction:str, kattr:dict={}, classMethod:bool=False):
        try:
            return self._action(sAction=sAction, kattr=kattr, classMethod=classMethod)
        except Exception as e:
            print(f"[ModuleManagerPkg] Вызов '{sAction}' завершился с ошибкой: {e}")

    def _getModule(self, sNameModule):
        return importlib.import_module(f'module.{sNameModule}')

    def _getClass(self, sNameClass):
        sNameModule = getModule(sNameClass)
        module = self._getModule(sNameModule)
        if not hasattr(module, sNameClass):
            raise AttributeError(f"Класс {sNameClass} не найден в модуле {sNameModule}")
            
        return getattr(module, sNameClass)
        
    def getClassByName(self, sNameClass:str):
        from core.empty.pub import EmptyPub
        pub:EmptyPub = self._getClass(sNameClass)
        return pub

    def getMetaCache(self, sNameMetaFile:str)->dict:
        sNameModule = getModule(sNameMetaFile)
        module = self._getModule(sNameModule)
        return getattr(module, 'META_FILE')

    def getNameModule(self)->list[str]:
        try:
            projects = asyncRun(FileManagerPkg.ReadFile(self._PATH_PROJECT))
        except Exception:
            return []
        return (projects or {}).get('modules', [])

    def getModulesHooks(self) -> dict:
        return self._getModulesInfo(self._PATH_HOOKS)

    def getModulesConfig(self) -> dict:
        return self._getModulesInfo(self._PATH_APP_CONFIG)

    def _getModulesInfo(self, sPath) -> dict:
            result = {}
            for name in self.getNameModule():
                conf = self._getModuleInfo(name, sPath)
                if isinstance(conf, dict):
                    result[name] = conf
            return result

    def _getModuleInfo(self, moduleName:str, sPath):
        """Читает hooks.json одного модуля или возвращает None."""
        path = sPath.format(module=moduleName)
        try:
            conf = asyncRun(FileManagerPkg.ReadFile(path))
        except Exception:
            return None
        return conf if isinstance(conf, dict) else None

    def runHook(self, hookName:str, **arg):
        """Вызывает optional-хук (например 'on_startup') из hooks.json каждого модуля.

        Значение хука — строка вида 'Class.method' (тот же контракт, что и action()).
        Ошибка в одном модуле не роняет приложение и не блокирует остальные модули.
        """
        if self.cacheHooks == {}:
            self.cacheHooks = self.getModulesHooks()
        for moduleName, conf in self.cacheHooks.items():
            sAction = conf.get(hookName)
            if not sAction:
                continue
            try:
                self._action(sAction=sAction['name'], kattr=arg, classMethod=sAction['isClassMetod'])
            except Exception as e:
                print(f"[ActionDispatcher] Хук '{hookName}' модуля '{moduleName}' "
                      f"завершился с ошибкой: {e}")
        
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
        
