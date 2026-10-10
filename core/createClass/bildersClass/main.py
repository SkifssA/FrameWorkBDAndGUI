from pathlib import Path
import re

from .bilderLogic import BilderLogic
from .bilderPub import BilderPub
from .bilderDvi import BilderDvi
from .bilderDpi import BilderDpi
from .bilderAmeta import BildersAmeta
from .bildersDmeta import BildersDmeta

from core.package.FileManager import FileManagerPkg
from core.package.ModuleManagerPkg import ModuleManagerPkg
from core.fabric.MetaInfo import MetaInfo
from core import asyncRun

pathModile = lambda app, end='': f"module/{app}" + end

def createFile(sPath: str):
    '''Создание файлов для класса'''
    lFiles = asyncRun(FileManagerPkg.getFilesWithExtension(sPath, '.odb.json'))
    for File in lFiles:
        app, dirName, cl = re.findall(r'module/(\w+)/\w+/(\w+)/([^.]+)', File.as_uri())[0]
        print(app, dirName, cl)
        
        module = ModuleManagerPkg()._getModule(app)
        metaFile = getattr(module, 'META_FILE')

        data = MetaInfo().getMetaTab(File.__str__())
        pathPyFile = pathModile(app, f"/object/{dirName}")
        print(f"Запись в Dpi в классе {dirName}")
        asyncRun(BilderDpi(data).createFileD(pathPyFile))
        print(f"Запись в Dvi в классе {dirName}")
        asyncRun(BilderDvi(data).createFileD(pathPyFile))
        print(f"Запись в Logic в классе {dirName}")
        asyncRun(BilderLogic(data).createFileA(pathPyFile))
        print(f"Запись в Pub в классе {dirName}")
        asyncRun(BilderPub(data).createFileA(pathPyFile))

        pathMetaFile = pathModile(app, f"/schemas/{dirName}")
        metaFile = metaFile | asyncRun(BildersDmeta(data).createFile(pathMetaFile))
        metaFile = metaFile | asyncRun(BildersAmeta(data).createFile(pathMetaFile))

    # asyncRun(FileManagerPkg.CreateFile(pathModile(app, '/cache/meta.json'), metaFile))
    # asyncRun(_getInitModule(app))

async def _getInitModule(app):
    dir = pathModile(app, "/object")
    w = await FileManagerPkg.getFilesWithExtension(dir, '.py')
    paths = [f for f in w if not (f.stem.endswith('Dvi') or f.stem.endswith('Dpi'))]
    base_path = Path(FileManagerPkg._getObjPath(pathModile(app))['real_path'])
    imports = []
    classLogic = []
    for p in paths:
        # Относительный путь от base_path (без расширения .py)
        rel_path = p.relative_to(base_path).with_suffix('')
        # Преобразуем в строку и заменяем '/' или '\' на '.'
        module_path = str(rel_path).replace('/', '.').replace('\\', '.')
        # Имя класса — последняя часть имени файла
        class_name = p.stem  # то же, что и rel_path.name
        # Формируем строку импорта
        import_line = f'from .{module_path} import {class_name}'
        classLogic.append(f'\'{class_name}\'')
        imports.append(import_line)
    
    await FileManagerPkg.CreateFile(pathModile(app, "/__init__.py"), '\n'.join(imports) + 
                                    f'\n\nfrom core.sdk import FileManagerPkg, asyncRun\nMETA_FILE = asyncRun(FileManagerPkg.ReadFile(\'{pathModile(app, '/cache/meta.json')}\'))' +
                                    f'\n\n__all__ = [\n    {'\n    ,'.join(classLogic)}\n]')