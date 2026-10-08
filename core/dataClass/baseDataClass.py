from dataclasses import dataclass, asdict, is_dataclass, fields

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
                l = [item for item in cleaned_list if item is not None]

                return l if l != [] else None
                
            # Если это словарь, убираем ключи с None
            if isinstance(value, dict):
                return {k: x for k, v in value.items() if (x:=_clean(v)) is not None}
                
            # Возвращаем обычное значение
            return value 

        if isNotNone:
            return _clean(asdict(self))
        return asdict(self)

    def merge(self, other: 'Base') -> 'Base':
        """
        Глубокое слияние двух датаклассов.
        Приоритет у значений из 'other'.
        Списки объектов сливаются по полю 'name' (если оно есть).
        """
        if not is_dataclass(other):
            return other

        current_data = {}
        
        for f in fields(self):
            key = f.name
            curr_val = getattr(self, key)
            other_val = getattr(other, key, None)

            # 1. Если в other значение None, берем текущее
            if other_val is None:
                current_data[key] = curr_val
                continue

            # 2. Рекурсия для вложенных датаклассов
            if is_dataclass(curr_val) and is_dataclass(other_val):
                current_data[key] = curr_val.merge(other_val)
            
            # 3. Обработка списков датаклассов (самое сложное)
            elif isinstance(curr_val, list) and isinstance(other_val, list):
                current_data[key] = self._merge_lists(curr_val, other_val)
                
            # 4. Обычные типы (строки, числа, bool) - просто заменяем
            else:
                current_data[key] = other_val

        return self.__class__(**current_data)

    def _merge_lists(self, current_list: list, new_list: list) -> list:
        """
        Сливаем два списка датаклассов.
        Ищем совпадения по полю 'name'. Если нет 'name', просто заменяем список.
        """
        if not new_list:
            return current_list
        
        if not current_list:
            return new_list

        # Проверяем, являются ли элементы списка датаклассами с полем 'name'
        if current_list and is_dataclass(current_list[0]) and hasattr(current_list[0], 'name'):
            # Создаем словарь для быстрого поиска: {name: object}
            curr_map = {item.name: item for item in current_list if item.name}
            new_map = {item.name: item for item in new_list if item.name}
            
            merged_items = []
            processed_names = set()

            # 1. Берем все элементы из new_list (они имеют приоритет)
            for name, new_item in new_map.items():
                if name in curr_map:
                    # Элемент есть везде -> мержим их
                    merged_items.append(curr_map[name].merge(new_item))
                else:
                    # Элемент только новый -> добавляем как есть
                    merged_items.append(new_item)
                processed_names.add(name)

            # 2. Добавляем элементы из current_list, которых не было в new_list
            for name, curr_item in curr_map.items():
                if name not in processed_names:
                    merged_items.append(curr_item)
                    
            # Сохраняем порядок? Обычно лучше отсортировать по order или оставить как в new
            # Для простоты вернем объединенный список
            return merged_items
        else:
            # Если это список простых типов или без поля name - просто заменяем
            return new_list if new_list else current_list