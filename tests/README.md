# Тесты core

Запуск: `python -m pytest` (из корня проекта).

| Файл | Что покрывает |
|---|---|
| core/test_module_manager.py | Контракт sAction, приватные методы, изоляция ошибок в action()/runHook() |
| core/test_sql_logic.py | Антиинъекционная валидация идентификаторов, параметризованный SQL, NULL |
| core/test_dataclass_base.py | Base.getDict (очистка) и Base.merge (приоритет other, слияние списков по name) |
| core/test_meta_info.py | Парсинг *.odb.json / мета UI в датаклассы, round-trip, getSQL() |
| core/test_oper_registry.py | Атрибуты @Oper/@Setter, сортировка по order, корни/дети, фильтрация скрытых |
| core/test_bilders.py | Golden-текст Dpi/Logic, createFileA не перезаписывает ручной код, fallback на id |
| core/test_lazy_val.py | Ленивость дескриптора, проксирование атрибутов, dunder-защита |
| core/test_file_manager.py | JSON/YAML/text round-trip, Exists, GetFoldersList, поиск *.odb.json |

Примечания:
* Реальная БД не используется: фикстура `monkeypatch_sql` (tests/conftest.py)
  перехватывает ASQL/ATSQL **в пространстве имён `core.DB.SQLLogic`** — именно
  оттуда они вызываются (import by value).
* В test_module_manager зафиксировано текущее поведение `getModule()` для имён
  без `_` (теряется последний символ) — регрессионный маркер потенциального бага.
