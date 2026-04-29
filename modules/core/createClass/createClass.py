from ....engine.package import FileManagerPkg, ASQL, ATQSL, ActionDispatcher
from collections import Counter

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
    listApp = await FileManagerPkg.ReadFile("../../project.yaml")
    script = []
    for app in listApp['modules']:
        pathClass = f"../../modules/{app}/schemas"
        if await FileManagerPkg.Exists(pathClass):
                for cl in await FileManagerPkg.GetFoldersList(pathClass):
                    lFiles = await FileManagerPkg.getFilesWithExtension(f'{pathClass}/{cl}', '.odb.json')
                    for File in lFiles:
                        w = await FileManagerPkg.ReadFile(File.__str__())
                        await __insertTab(w)
                        # Выполнение скриптов для заполнения таблиц
                        if 'dbData' in w.keys():
                            for i in w['dbData']:
                                script.append(i)
                    lFilesPkg = await FileManagerPkg.getFilesWithExtension(f'{pathClass}', '.pkg.json')
                    for filePkg in lFilesPkg:
                        w = await FileManagerPkg.ReadFile(filePkg.__str__())
                        if 'dbData' in w.keys():
                            for i in w['dbData']:
                                script.append(i)

    await __actionScripts(script)

async def __insertTab(data):
    from ..object.clas.ClassApi import ClassApi
    # Проверяем, существует ли таблица в meta_tables
    existing_id = await ClassApi()._findByAttr('sCode', data['name'])
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
        CREATE INDEX IF NOT EXISTS index_{nameTable}{'_new' if isNew else ''}_mnemocode ON {nameTable}{'_new' if isNew else ''} (sMnemoCode);
        """)
    print(f'Генерация index_{nameTable}{'_new' if isNew else ''}_mnemocode прошла успешно')

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
        await ATQSL(f"DROP TABLE IF EXISTS {nameTable}")
        await ATQSL(f"DROP INDEX IF EXISTS {nameTable}_new_mnemocode")

        # Переименовываем новую
        await ATQSL(f"ALTER TABLE {nameTable}_new RENAME TO {nameTable}")
        await ATQSL(f"""
            CREATE INDEX IF NOT EXISTS index_{nameTable}_mnemocode ON {nameTable} (sMnemoCode);
        """)
    else:
        # Если таблицы не было — создаём её как обычно
        await __createTable(q, nameTable, False)

async def __actionScripts(datas:list[dict]):

    async def actionDependence(sName):
        w = next((d for d in datas if d.get("name") == sName), None)
        await __actionScripts([w])

    for data in datas:
        d = await ASQL(f"SELECT nVersion FROM Script WHERE sAction = ?", (data['name'], ))
        if d == [] or d[0]['nVersion'] < data['version']:
            if 'dependence' in data.keys():
                if isinstance(data['dependence'], list):
                    for depe in data['dependence']:
                        await actionDependence(depe)
                else:
                    await actionDependence(data['dependence'])
            await ActionDispatcher().action(data['name'])
            if d == []:
                s = f"INSERT INTO Script (nVersion, sAction) VALUES (?, ?)"
            else:
                s = f"UPDATE Script SET nVersion = ? WHERE sAction = ?"
            await ATQSL(s, (data['version'], data['name']))