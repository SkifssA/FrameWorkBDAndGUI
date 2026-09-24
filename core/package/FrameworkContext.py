import sys
from typing import Optional, Any, Callable
from core.ui.forms.base import Base

class FrameworkContext:
    @staticmethod
    def find_parent_form(obj: Any,
                    *,
                    exclude_same_hierarchy: bool = True,
                    custom_filter: Optional[Callable[[Any], bool]] = None) -> Optional[Base]:
        """
        Находит родителя в стеке вызовов.
        
        Args:
            obj: Текущий объект
            exclude_same_hierarchy: Исключать ли объекты из той же иерархии классов
            custom_filter: Дополнительная фильтрация
        """
        from core.fabric.Form import FormConstruct
        frame = sys._getframe().f_back
        obj_class = type(obj)
        
        while frame:
            self_obj = frame.f_locals.get('self')
            if (issubclass(type(self_obj), FormConstruct)):
                self_obj = self_obj.clsForm

            if self_obj and self_obj is not obj and (issubclass(type(self_obj), Base)):
                # Проверка на иерархию
                if exclude_same_hierarchy:
                    # Пропускаем, если obj и self_obj из одной иерархии
                    if issubclass(obj_class, type(self_obj)) or issubclass(type(self_obj), obj_class):
                        frame = frame.f_back
                        continue
                
                # Применяем пользовательский фильтр
                if custom_filter is None or custom_filter(self_obj):
                    return self_obj
            
            frame = frame.f_back
        
        return None