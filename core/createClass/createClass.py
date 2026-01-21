from ..package import Core_FileManagerPkg, ASQL, ATQSL, Core_ActionDispatcherPkg
from .bilders import BilderApi, BilderAvi, BilderDvi, BilderDpi, BildersAmeta, BildersDmeta
from collections import Counter
from pathlib import Path

TYPE_MAPPING = {
    "TEXT": "TEXT",
    "STRING": "TEXT",
    "INT": "INTEGER",
    "INTEGER": "INTEGER",
    "LONG": "INTEGER",
    "BOOLEAN": "INTEGER",
    "DATE": "TEXT",
}

async def createTab():
    await __initMetaTab()
    listApp = await Core_FileManagerPkg.ReadFile("../../project.yaml")
    script = []
    for app in listApp['modules']:
        pathClass = f"../../{app}/schemas"
        if await Core_FileManagerPkg.Exists(pathClass):
                for cl in await Core_FileManagerPkg.GetFoldersList(pathClass):
                    lFiles = await Core_FileManagerPkg.getFilesWithExtension(f'{pathClass}/{cl}', '.odb.json')
                    for File in lFiles:
                        w = await Core_FileManagerPkg.ReadFile(File.__str__())
                        await __insertTab(w)
                        # Выполнение скриптов для заполнения таблиц
                        if 'dbData' in w.keys():
                            for i in w['dbData']:
                                script.append(i)
                    lFilesPkg = await Core_FileManagerPkg.getFilesWithExtension(f'{pathClass}', '.pkg.json')
                    for filePkg in lFilesPkg:
                        w = await Core_FileManagerPkg.ReadFile(filePkg.__str__())
                        if 'dbData' in w.keys():
                            for i in w['dbData']:
                                script.append(i)

    await __actionScripts(script)

async def createFile():
    listApp = await Core_FileManagerPkg.ReadFile("../../project.yaml")
    for app in listApp['modules']:
        pathClass = f"../../modules/{app}/schemas"
        if await Core_FileManagerPkg.Exists(pathClass):
            for cl in await Core_FileManagerPkg.GetFoldersList(pathClass):
                lFiles = await Core_FileManagerPkg.getFilesWithExtension(f'{pathClass}/{cl}', '.odb.json')
                for File in lFiles:
                    data = await Core_FileManagerPkg.ReadFile(File.__str__())
                    await BilderDpi(data).createFile(f'../../../modules/{app}/object/{cl}')
                    await BilderDvi(data).createFile(f'../../../modules/{app}/object/{cl}')
                    await BilderApi(data).createFile(f'../../../modules/{app}/object/{cl}')
                    await BilderAvi(data).createFile(f'../../../modules/{app}/object/{cl}')

                    await BildersDmeta(data).createFile(f'../{pathClass}/{cl}')
                    await BildersAmeta(data).createFile(f'../{pathClass}/{cl}')

            print(await _test(app))


async def _test(app):
    dir = f"../../modules/{app}/object"
    w = await Core_FileManagerPkg.getFilesWithExtension(dir, '.py')
    paths = [f for f in w if not (f.stem.endswith('Dvi') or f.stem.endswith('Dpi'))]
    base_path = Path(Core_FileManagerPkg._getObjPath(f"../../modules/{app}")['real_path'])
    imports = []
    for p in paths:
        # Относительный путь от base_path (без расширения .py)
        rel_path = p.relative_to(base_path).with_suffix('')
        # Преобразуем в строку и заменяем '/' или '\' на '.'
        module_path = str(rel_path).replace('/', '.').replace('\\', '.')
        # Имя класса — последняя часть имени файла
        class_name = p.stem  # то же, что и rel_path.name
        # Формируем строку импорта
        import_line = f'from .{module_path} import {class_name}'
        imports.append(import_line)
    
    await Core_FileManagerPkg.CreateFile(f"../../modules/{app}/__init__.py", '\n'.join(imports))

    return imports

async def __initMetaTab():
    for i in await Core_FileManagerPkg.getFilesWithExtension(f'../../core/schemas/clas', '.odb.json'):
        data = await Core_FileManagerPkg.ReadFile(i.__str__())
        q = await __getQ(None, data['attr'])
        await __createOrUpdateTable(q, data['attr'], data['name'], False)
        await ASQL("INSERT OR IGNORE INTO Core_Class (sCode, sMnemoCode) VALUES (?, ?)", (data['name'],data['name'],))

    for i in await Core_FileManagerPkg.getFilesWithExtension(f'../../core/schemas/attr', '.odb.json'):
        data = await Core_FileManagerPkg.ReadFile(i.__str__())
        q = await __getQ(None, data['attr'])
        await __createOrUpdateTable(q, data['attr'], data['name'], False)
        await ASQL("INSERT OR IGNORE INTO Core_Class (sCode, sMnemoCode) VALUES (?, ?)", (data['name'],data['name'],))

async def __insertMetaTable(sName, sCaption):
    from ..object.clas.Core_ClassApi import Core_ClassApi
    rop = await Core_ClassApi().register(sName, sCaption)
    return rop.id

async def __insertMetaColumn(idTab, sName, sType, sCaption, sNameRefTab=None):
    from ..object.attr.Core_AttrApi import Core_AttrApi
    await Core_AttrApi().register(idTab, sName, sType, sCaption, sNameRefTab)

async def __insertTab(data):
    from ..object.clas.Core_ClassApi import Core_ClassApi
    # Проверяем, существует ли таблица в meta_tables
    existing_id = await Core_ClassApi()._findByAttr('sCode', data['name'])
    table_existed = bool(existing_id)

    data['id'] = await __insertMetaTable(data['name'], data['caption'])

    q = await __getQ(data['id'], data['attr'])

    if table_existed:
        old_columns = await ASQL(f"PRAGMA table_info({data['name']})")
        old_col_names = [row['name'] for row in old_columns]
        new_col_names = [i['name'] for i in data['attr']] + ['id', 'gid', 'sHeadLine', 'sMnemoCode']

        if Counter(old_col_names) == Counter(new_col_names):
            print("Новых столбцов нет")
            return data

    # Вставляем в meta_tables
    

    await __insertMetaColumn(data['id'], 'id', 'INTEGER', 'Идентификатор')
    await __insertMetaColumn(data['id'], 'gid', 'TEXT', 'Глобальный идентификатор')
    await __insertMetaColumn(data['id'], 'sHeadLine', 'TEXT', 'sHeadLine')
    await __insertMetaColumn(data['id'], 'sMnemoCode', 'TEXT', 'sMnemoCode')
    
    await __createOrUpdateTable(q, data['attr'], data['name'], table_existed)

    return data

async def __getQ(idTabl, dataAttr):
    q = {
        'attr': []
    }

    for i in dataAttr:
        q['attr'].append(f"{i['name']} {TYPE_MAPPING[i['type'].upper()]}")
        if 'refTab' in i:
            c = i['refTab']
        else:
            c = None
        if idTabl:
            await __insertMetaColumn(idTabl, i['name'], TYPE_MAPPING[i['type'].upper()], i['caption'], c)
    
    return q

async def __createTable(q, nameTable, isNew):
    await ATQSL(f"""
            CREATE TABLE IF NOT EXISTS {nameTable}{'_new' if isNew else ''} (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                gid TEXT,
                sHeadLine TEXT,
                sMnemoCode TEXT UNIQUE,
                {',\n    '.join(q['attr'])}
            )
        """)
    
    await ATQSL(f"""
        CREATE INDEX IF NOT EXISTS index_{nameTable}_mnemocode ON {nameTable} (sMnemoCode);
        """)
    print(f'Генерация index_{nameTable}_mnemocode прошла успешно')

async def __createOrUpdateTable(q, dataAttr, nameTable, isExisted):
    # Если таблица уже существовала, нужно перенести данные
    if isExisted:
        # Получаем список старых столбцов (для переноса данных)
        old_columns = await ASQL(f"PRAGMA table_info({nameTable})")
        old_col_names = [row['name'] for row in old_columns]
        new_col_names = [i['name'] for i in dataAttr] + ['id', 'gid', 'sHeadLine', 'sMnemoCode']

        if Counter(old_col_names) == Counter(new_col_names):
            print("Новых столбцов нет")
            # return

        # Создаём новую таблицу с новой структурой
        await __createTable(q, nameTable, True)

        # Копируем данные из старой в новую (только общие столбцы)
        common_columns = [col for col in old_col_names if col in new_col_names]
        if common_columns:
            columns_str = ', '.join(common_columns)
            await ATQSL(f"""
                INSERT INTO {nameTable}_new ({columns_str})
                SELECT {columns_str} FROM {nameTable}
            """)

        # Удаляем старую таблицу
        await ATQSL(f"DROP TABLE {nameTable}")

        # Переименовываем новую
        await ATQSL(f"ALTER TABLE {nameTable}_new RENAME TO {nameTable}")
    else:
        # Если таблицы не было — создаём её как обычно
        await __createTable(q, nameTable, False)

async def __actionScripts(datas:list[dict]):

    async def actionDependence(sName):
        w = next((d for d in datas if d.get("name") == sName), None)
        await __actionScripts([w])

    for data in datas:
        d = await ASQL(f"SELECT nVersion FROM Core_Script WHERE sAction = ?", (data['name'], ))
        if d == [] or d[0]['nVersion'] < data['version']:
            if 'dependence' in data.keys():
                if isinstance(data['dependence'], list):
                    for depe in data['dependence']:
                        await actionDependence(depe)
                else:
                    await actionDependence(data['dependence'])
            await Core_ActionDispatcherPkg().action(data['name'])
            if d == []:
                s = f"INSERT INTO Core_Script (nVersion, sAction) VALUES (?, ?)"
            else:
                s = f"UPDATE Core_Script SET nVersion = ? WHERE sAction = ?"
            await ATQSL(s, (data['version'], data['name']))