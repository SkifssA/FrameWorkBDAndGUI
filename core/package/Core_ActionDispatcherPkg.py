import importlib
import inspect

class Core_ActionDispatcherPkg:
    async def action(self, sAction:str):
        sNameClass, sNameMetod = sAction.split('.')
        sNameModule = f'{sNameClass[:sNameClass.find('_')].lower()}.object.{sNameClass}'
        try:
            module = importlib.import_module(sNameModule)
            if not hasattr(module, sNameClass):
                raise AttributeError(f"Класс {sNameClass} не найден в модуле {sNameModule}")
            cls =  getattr(module, sNameClass)

            if not hasattr(cls, sNameMetod):
                raise AttributeError(f"Метод {sNameMetod} не найден в классе {sNameClass}")
            attr = getattr(cls(), sNameMetod)
            if inspect.iscoroutinefunction(attr):
                # Это async def метод → вызываем и ждём
                return await attr()
            elif callable(attr):
                # Обычный метод
                return attr()
        except ImportError as e:
            raise ValueError(f"Не удалось импортировать модуль {sNameModule}: {e}")
        
