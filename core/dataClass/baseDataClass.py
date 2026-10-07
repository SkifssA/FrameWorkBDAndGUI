from dataclasses import dataclass, asdict, is_dataclass

@dataclass
class Base:
    def getDict(self, isNotNone:bool=True)->dict:

        def _clean(value):
            # Если это вложенный dataclass, обрабатываем его рекурсивно
            if is_dataclass(value):
                return value.getDict()
            
            # Если это список или кортеж, чистим каждый элемент внутри
            if isinstance(value, (list, tuple)):
                cleaned_list = [_clean(item) for item in value]
                # Убираем из списка элементы, которые стали None после очистки
                return [item for item in cleaned_list if item is not None]
                
            # Если это словарь, убираем ключи с None
            if isinstance(value, dict):
                return {k: _clean(v) for k, v in value.items() if v is not None}
                
            # Возвращаем обычное значение
            return value

        if isNotNone:
            return _clean(asdict(self))
        return asdict(self)

    def merge(self, other: 'Base'):
        """Объединяет текущий объект с другим, приоритет у 'other'."""
        # Получаем словарь текущего объекта
        current_data = asdict(self)
        # Получаем словарь того, что хотим наложить сверху
        new_data = asdict(other)
        
        # Обновляем: если в new_data есть значение (и оно не None), оно заменит старое
        for key, value in new_data.items():
            if value is not None: 
                current_data[key] = value
                
        return Base(**current_data)