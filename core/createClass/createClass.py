from ..package import Core_FileManagerPkg, ASQL, ATQSL, Core_ActionDispatcherPkg
from .templace import Api, Avi, Dpi, Dvi
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
    script = []
    for app in listApp['modules']:
        pathClass = f"../../{app}/schemas"
        if await Core_FileManagerPkg.Exists(pathClass):
                for cl in await Core_FileManagerPkg.GetFoldersList(pathClass):
                    lFiles = await Core_FileManagerPkg.getFilesWithExtension(f'{pathClass}/{cl}', '.odb.json')
                    for File in lFiles:
                        data = await Core_FileManagerPkg.ReadFile(File.__str__())
                        await _createFileProg(f'../../{app}/object/{cl}', data)
                        await _createFileMeta(f'../../{app}/schemas/{cl}', data)

async def _createFileProg(path, data):
     data = await _createDataForFile(data)
     await __createDpi(path, data)
     await __createApi(path, data)
     await __createDvi(path, data)
     await __createAvi(path, data)

async def _createFileMeta(path, data):
    print(data['name'])
    print(data['caption'])
    print(data['attr'])
    print(data['showAttr'])

    pathWhitFileD = f'{path}/{data['name']}.Dmeta.json'
    pathWhitFileA = f'{path}/{data['name']}.Ameta.json'

    if not await Core_FileManagerPkg.Exists(pathWhitFileA):
        fA = {}
        await Core_FileManagerPkg.CreateFile(pathWhitFileA, fA)

    attr = {
        'id': {
                'caption': 'id',
                'edit': 'edit',
                'isVisible': False
            },
        'gid': {
                'caption': 'gid',
                'edit': 'edit',
                'isVisible': False
            }
        }
    
    for i in data['attr']:
        attr[i['name']] = {
                "caption": i['caption'],
                "edit": i['editType'] if 'editType' in i else 'edit',
                'isVisible': i['name'] in data['showAttr']
            }
        if i['name'].startswith('id'):
            attr[i['name']+'HL'] = {
                "caption": i['caption'],
                "edit": i['editType'] if 'editType' in i else 'edit',
                'isVisible': i['name']+'HL' in data['showAttr']
            }
        if  'editType' in i:
            if i['editType'] == 'lookUp':
               attr[i['name']+'HL']['display'] = 'LookUp'
               attr[i['name']+'HL']['refTab'] = i['refTab']
        

    fD = {'Default':{
            'caption': data['caption'],
            'attr': attr
        }}
    await Core_FileManagerPkg.CreateFile(pathWhitFileD, fD)

async def __createApi(path, data):
     pathWhitFile = f'{path}/{data['name']}Api.py'
     if not await Core_FileManagerPkg.Exists(pathWhitFile):
        f = Api.format(nameClass=data['name'])
        await Core_FileManagerPkg.CreateFile(pathWhitFile, f)

async def __createAvi(path, data):
     pathWhitFile = f'{path}/{data['name']}Avi.py'
     if not await Core_FileManagerPkg.Exists(pathWhitFile):
        f = Avi.format(nameClass=data['name'])
        await Core_FileManagerPkg.CreateFile(pathWhitFile, f)

async def __createDpi(path, data):
    pathWhitFile = f'{path}/{data['name']}Dpi.py'
    f = Dpi.format(nameClass=data['name'],
                   attr=f' = None\n{' '*8}self.'.join(data['attrRop']), 
                   isHeadLine=data['isHeadLine'],
                   isMnemoCode=data['isMnemoCode'],
                   deleteDetails=data['deleteDetails'])
    await Core_FileManagerPkg.CreateFile(pathWhitFile, f)

async def __createDvi(path, data):
    pathWhitFile = f'{path}/{data['name']}Dvi.py'
    f = Dvi.format(nameClass=data['name'], sqlList=data['sqlList'], showAttr='\''+'\', \''.join(data['showAttr'])+'\'')
    await Core_FileManagerPkg.CreateFile(pathWhitFile, f)

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
    print(sName, sCaption)
    rop = await Core_ClassApi().register(sName, sCaption)
    return rop.id

async def __insertMetaColumn(idTab, sName, sType, sCaption, sNameRefTab=None):
    from ..object.attr.Core_AttrApi import Core_AttrApi
    await Core_AttrApi().register(idTab, sName, sType, sCaption, sNameRefTab)

async def _createDataForFile(data):
    data['sqlList'] = await __getSqlList(data['attr'], data['name'])
    data['attrRop'] = await __getRopAttr(data['attr'])
    data['isHeadLine'] = await __getHeadLine(data['attr'])
    data['isMnemoCode'] = await __getMnemoCode(data['attr'])
    data['showAttr'] = await __getShowAttr(data['attr'])
    data['deleteDetails'] = await __getDelete(data)
    return data

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
            print("Новых столбчов нет")
            return data

    # Вставляем в meta_tables
    

    await __insertMetaColumn(data['id'], 'id', 'INTEGER', 'Идентификатор')
    await __insertMetaColumn(data['id'], 'gid', 'TEXT', 'Глобальный идентификатор')
    await __insertMetaColumn(data['id'], 'sHeadLine', 'TEXT', 'sHeadLine')
    await __insertMetaColumn(data['id'], 'sMnemoCode', 'TEXT', 'sMnemoCode')
    
    await __createOrUpdateTable(q, data['attr'], data['name'], table_existed)

    return data

async def __getSqlList(dataAttr, nameTabl)->str:
    sqlstr = {
        'int': 1,
        'attr': ['t.id', 't.gid'],
        'join': []
    }
    for i in dataAttr:
        sqlstr['attr'].append(f"t.{i['name']}")
        if 'refTab' in i:
            sqlstr['attr'].append(f"t{sqlstr['int']}.sHeadLine as {i['name']}HL")
            sqlstr['join'].append(f"LEFT JOIN {i['refTab']} t{sqlstr['int']} ON t{sqlstr['int']}.id = t.{i['name']}")
            sqlstr['int'] += 1

    return f"""
            SELECT {',\n                   '.join(sqlstr['attr'])}
            FROM {nameTabl} AS t
                   {'\n                   '.join(sqlstr['join'])}
            """

async def __getRopAttr(dataAttr):
    rop = []
    for i in dataAttr:
        
        if i['name'].startswith('id') or i['name'].startswith('n') or i['name'].startswith('b'):
            typeAttr = 'int'
        elif i['name'].startswith('gid'):
            typeAttr = 'gid'
        else:
            typeAttr = 'str'


        rop.append(f'{i['name']}:{typeAttr}')
    return rop

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

async def __createOrUpdateTable(q, dataAttr, nameTable, isExisted):
    # Если таблица уже существовала, нужно перенести данные
    if isExisted:
        # Получаем список старых столбцов (для переноса данных)
        old_columns = await ASQL(f"PRAGMA table_info({nameTable})")
        old_col_names = [row['name'] for row in old_columns]
        new_col_names = [i['name'] for i in dataAttr] + ['id', 'gid', 'sHeadLine', 'sMnemoCode']

        if Counter(old_col_names) == Counter(new_col_names):
            print("Новых столбчов нет")
            return

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
        d = await ASQL(f"SELECT nVersion FROM Core_Script WHERE sAction = '{data['name']}'")
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

async def __getHeadLine(dataAttr):
    rop = []
    for i in dataAttr:
        if 'isHeadLine' in i:
            rop.append(f'rop.{i['name']}')
    return '{' + ('} {'.join(rop) if rop != [] else 'rop.id') + '}'

async def __getMnemoCode(dataAttr):
    rop = []
    for i in dataAttr:
        if 'isMnemoCode' in i:
            rop.append(f'rop.{i['name']}')
    return '{' + ('} {'.join(rop) if rop != [] else 'rop.id') + '}'

async def __getShowAttr(dataAttr):
    res = []
    for i in dataAttr:
        if 'isVisible' in i:
            if not i['isVisible']:
                continue
        res.append(i['name']+('HL' if i['name'].startswith('id') else ''))
    return res

async def __getDelete(data):
    res = []
    if 'collections' in data.keys():
        mM = data['name'][:data['name'].find('_')].lower()
        for i in data['collections']:
            w:str = i['name']
            m = i['name'][:i['name'].find('_')].lower()
            mtemp = '...' if mM == m else f'{m}.'
            res.append(f'from {mtemp}object.{w.split('_')[-1].lower()}.{w}Api import {w}Api')
            res.append(f'd = await {w}Api()._getAllByAttr(\'{i['attr']}\', rop.{'id' if i['attr'].startswith('id') else 'gid'})')
            res.append(f'if d: asyncio.gather(*({w}Api().delete(i) for i in d))')
            
    return '\n        '.join(res)
