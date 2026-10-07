from .bilderLogic import BilderLogic
from .bilderPub import BilderPub
from .bilderDvi import BilderDvi
from .bilderDpi import BilderDpi
from .bilderAmeta import BildersAmeta
from .bildersDmeta import BildersDmeta

from core.package.FileManager import FileManagerPkg
from core.fabric.MetaInfo import MetaInfo
from core import asyncRun
from pathlib import Path

pathModile = lambda app, end='': f"module/{app}" + end

def createFile():
    '''Создание файлов для класса'''
    listApp = asyncRun(FileManagerPkg.ReadFile("project.yaml"))
    for app in listApp['modules']:
        pathClass = pathModile(app, '/schemas')
        if asyncRun(FileManagerPkg.Exists(pathClass)):
            for cl in asyncRun(FileManagerPkg.GetFoldersList(pathClass)):
                lFiles = asyncRun(FileManagerPkg.getFilesWithExtension(f'{pathClass}/{cl}', '.odb.json'))
                for File in lFiles:
                    data = MetaInfo().getMetaTab(File.__str__())
                    pathPyFile = pathModile(app, f"/object/{cl}")
                    print(f"Запись в Dpi в классе {cl}")
                    asyncRun(BilderDpi(data).createFileD(pathPyFile))
                    print(f"Запись в Dvi в классе {cl}")
                    asyncRun(BilderDvi(data).createFileD(pathPyFile))
                    print(f"Запись в Logic в классе {cl}")
                    asyncRun(BilderLogic(data).createFileA(pathPyFile))
                    print(f"Запись в Pub в классе {cl}")
                    asyncRun(BilderPub(data).createFileA(pathPyFile))

                    pathMetaFile = f'{pathClass}/{cl}'
                    asyncRun(BildersDmeta(data).createFile(pathMetaFile))
                    asyncRun(BildersAmeta(data).createFile(pathMetaFile))

            asyncRun(_getInitModule(app))

async def _getInitModule(app):
    dir = pathModile(app, "/object")
    w = await FileManagerPkg.getFilesWithExtension(dir, '.py')
    paths = [f for f in w if not (f.stem.endswith('Dvi') or f.stem.endswith('Dpi'))]
    base_path = Path(FileManagerPkg._getObjPath(pathModile(app))['real_path'])
    imports = []
    classApi = []
    for p in paths:
        # Относительный путь от base_path (без расширения .py)
        rel_path = p.relative_to(base_path).with_suffix('')
        # Преобразуем в строку и заменяем '/' или '\' на '.'
        module_path = str(rel_path).replace('/', '.').replace('\\', '.')
        # Имя класса — последняя часть имени файла
        class_name = p.stem  # то же, что и rel_path.name
        # Формируем строку импорта
        import_line = f'from .{module_path} import {class_name}'
        classApi.append(f'\'{class_name}\'')
        imports.append(import_line)
    
    await FileManagerPkg.CreateFile(pathModile(app, "/__init__.py"), '\n'.join(imports) + f'\n\n__all__ = [\n    {'\n    ,'.join(classApi)}\n]')