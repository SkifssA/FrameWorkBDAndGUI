import importlib
import inspect

from core.package.AsynRun import asyncRun
from core.package.FileManager import FileManagerPkg

def getModule(nameClass: str)->str:
    return nameClass[:nameClass.find('_')].lower()

class ActionDispatcherPkg:
    _PATH_APP_CONFIG = "module/{module}/config/hooks.json"
    _PATH_PROJECT = "project.yaml"

    def __init__(self, IsRaise:bool=True):
        self.IsRaise = IsRaise
        self.cachHooks = {}

    def _action(self, sAction:str, kattr:dict={}, classMethod:bool=False):
        sNameClass, sNameMetod = sAction.split('.')
        sNameModule = f'module.{getModule(sNameClass)}'
        try:
            cls = self._getClass(sNameModule, sNameClass)
            if not hasattr(cls, sNameMetod):
                raise AttributeError(f"Метод {sNameMetod} не найден в классе {sNameClass}")
            
            attr = self._getMethod(cls, sNameMetod, classMethod)
            return self._runMethod(attr, kattr)
        except ImportError as e:
            if self.IsRaise:
                raise ValueError(f"Не удалось импортировать модуль {sNameModule}: {e}")

    def action(self, sAction:str, kattr:dict={}, classMethod:bool=False):
        try:
            return self._action(sAction=sAction, kattr=kattr, classMethod=classMethod)
        except Exception as e:
            print(f"[ActionDispatcher] Вызов '{sAction}' завершился с ошибкой: {e}")


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

    def getModulesConfig(self) -> dict:
        """Читает hooks.json всех модулей, перечисленных в project.yaml.

        Ключ — имя модуля, значение — содержимое module/<имя>/config/hooks.json.
        Модули без конфигурации (или с битым json) пропускаются.
        Путь разрешается относительно файла, из которого вызван метод,
        поэтому поведение совпадает с остальными обращениями к файлам в core.
        """
        result = {}
        try:
            projects = asyncRun(FileManagerPkg.ReadFile(self._PATH_PROJECT))
        except Exception:
            return result
        for name in (projects or {}).get('modules', []):
            conf = self.getModuleConfig(name)
            if isinstance(conf, dict):
                result[name] = conf
        return result

    def getModuleConfig(self, moduleName:str):
        """Читает hooks.json одного модуля или возвращает None."""
        path = self._PATH_APP_CONFIG.format(module=moduleName)
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
        if self.cachHooks == {}:
            self.cachHooks = self.getModulesConfig()
        for moduleName, conf in self.cachHooks.items():
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
        
