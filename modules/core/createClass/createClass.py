import logging
from typing import Dict, List, Any, Optional
from pathlib import Path
from engine.package import FileManagerPkg, ASQL, ATQSL, ActionDispatcher

logger = logging.getLogger(__name__)

TYPE_MAPPING: Dict[str, str] = {
    "TEXT": "TEXT", "STRING": "TEXT",
    "INT": "INTEGER", "INTEGER": "INTEGER", "LONG": "INTEGER",
    "BOOLEAN": "INTEGER", "DATE": "TEXT",
}

SYSTEM_COLUMNS: List[str] = ["id", "gid", "sHeadLine", "sMnemoCode"]
BASE_PATH = Path(__file__).resolve().parent.parent.parent  # Заменяет ../../

async def create_tables() -> None:
    """Главная точка входа: чтение конфигов, миграция таблиц, выполнение скриптов."""
    project_path = BASE_PATH / "project.yaml"
    if not await FileManagerPkg.Exists(project_path):
        logger.error("Файл project.yaml не найден по пути %s", project_path)
        return

    list_app = await FileManagerPkg.ReadFile(project_path)
    if not isinstance(list_app, dict) or "modules" not in list_app:
        logger.error("Некорректная структура project.yaml")
        return

    data_scripts: List[Dict[str, Any]] = []

    for app_name in list_app["modules"]:
        schema_dir = BASE_PATH / "modules" / app_name / "schemas"
        if not await FileManagerPkg.Exists(schema_dir):
            continue

        for schema_dir_name in await FileManagerPkg.GetFoldersList(schema_dir):
            dir_path = schema_dir / schema_dir_name
            
            # 1. Обработка .odb.json
            for odb_file in await FileManagerPkg.getFilesWithExtension(dir_path, ".odb.json"):
                schema = await FileManagerPkg.ReadFile(str(odb_file))
                if await _validate_schema(schema, str(odb_file)):
                    await __insert_table(schema)
                    if "dbData" in schema:
                        data_scripts.extend(schema["dbData"])

            # 2. Обработка .pkg.json
            for pkg_file in await FileManagerPkg.getFilesWithExtension(schema_dir, ".pkg.json"):
                pkg = await FileManagerPkg.ReadFile(str(pkg_file))
                if "dbData" in pkg:
                    data_scripts.extend(pkg["dbData"])

    if data_scripts:
        logger.info("Запуск %d скриптов заполнения данных", len(data_scripts))
        await __action_scripts(data_scripts)

async def __insert_table(data: Dict[str, Any]) -> None:
    """Регистрация метаданных и запуск миграции таблицы."""
    from ..object.clas.ClassApi import ClassApi

    # Проверка в метаданных (можно заменить на ASQL PRAGMA для надёжности)
    existing = await ClassApi()._findByAttr("sCode", data["name"])
    table_in_meta = bool(existing)

    meta_id = await __insert_meta_table(data["name"], data.get("caption", ""))
    data["id"] = meta_id

    query_schema = await __build_query_schema(meta_id, data["attr"])
    await __create_or_update_table(query_schema, data["attr"], data["name"], table_in_meta)

async def __build_query_schema(table_id: int, attributes: List[Dict]) -> Dict[str, List[str]]:
    """Формирует SQL-фрагменты колонок и записывает их в meta_columns."""
    cols_sql = []
    for attr in attributes:
        col_type = TYPE_MAPPING.get(attr["type"].upper(), "TEXT")
        cols_sql.append(f'"{attr["name"]}" {col_type}')
        
        await __insert_meta_column(
            table_id, 
            attr["name"], 
            col_type, 
            attr.get("caption", ""), 
            attr.get("refTab")
        )
    return {"attr": cols_sql}

async def __create_or_update_table(
    q: Dict[str, List[str]], 
    attr_data: List[Dict], 
    table_name: str, 
    exists_in_meta: bool
) -> None:
    """Создаёт таблицу или выполняет безопасную миграцию структуры."""
    safe_name = f'"{table_name}"'
    
    # Проверяем реальное наличие в БД
    pragma_rows = await ASQL(f"PRAGMA table_info({safe_name})")
    db_exists = len(pragma_rows) > 0

    if not db_exists:
        await __create_table(q, table_name, is_new=False)
        return

    old_cols = {row["name"] for row in pragma_rows}
    new_cols = {a["name"] for a in attr_data} | set(SYSTEM_COLUMNS)

    if old_cols == new_cols and len(old_cols) == len(new_cols):
        logger.debug("Структура таблицы %s не изменилась, пропуск", table_name)
        return

    logger.info("Обнаружены изменения в %s. Запуск миграции...", table_name)
    temp_name = f'"{table_name}_new"'

    try:
        # 1. Создаём новую таблицу
        await __create_table(q, table_name, is_new=True)
        
        # 2. Копируем данные только по общим колонкам
        common_cols = [f'"{c}"' for c in old_cols if c in new_cols]
        if common_cols:
            cols_str = ", ".join(common_cols)
            await ATQSL(f"INSERT INTO {temp_name} ({cols_str}) SELECT {cols_str} FROM {safe_name}")
            
        # 3. Удаляем старый индекс и таблицу
        await ATQSL(f'DROP INDEX IF EXISTS "index_{table_name}_mnemocode"')
        await ATQSL(f"DROP TABLE {safe_name}")
        
        # 4. Переименовываем и создаём индекс
        await ATQSL(f"ALTER TABLE {temp_name} RENAME TO {safe_name}")
        await __create_index(table_name)
        
        logger.info("Миграция таблицы %s завершена успешно", table_name)
    except Exception as e:
        logger.error("Ошибка миграции %s: %s. Откат не реализован (требует транзакций на уровне ASQL)", table_name, e)
        # В реальном проекте здесь должен быть rollback через ATQSL("ROLLBACK")

async def __create_table(q: Dict[str, List[str]], name_table: str, is_new: bool) -> None:
    suffix = "_new" if is_new else ""
    safe_name = f'"{name_table}{suffix}"'
    
    columns = ",\n    ".join(q["attr"])
    await ATQSL(f"""
        CREATE TABLE {safe_name} (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            gid TEXT,
            sHeadLine TEXT,
            sMnemoCode TEXT UNIQUE,
            {columns}
        )
    """)
    await __create_index(name_table, suffix)
    logger.info("Таблица %s создана", safe_name)

async def __create_index(name_table: str, suffix: str = "") -> None:
    idx_name = f"index_{name_table}{suffix}_mnemocode"
    safe_name = f'"{name_table}{suffix}"'
    await ATQSL(f'CREATE INDEX IF NOT EXISTS "{idx_name}" ON {safe_name} (sMnemoCode)')

async def _validate_schema(data: Any, file_path: str) -> bool:
    if not isinstance(data, dict) or "name" not in data or "attr" not in data:
        logger.error("Файл %s не содержит обязательных полей name/attr", file_path)
        return False
    return True