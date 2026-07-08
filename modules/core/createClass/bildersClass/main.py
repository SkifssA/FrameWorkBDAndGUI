from .bilderApi import BilderApi
from .bilderAvi import BilderAvi
from .bilderDvi import BilderDvi
from .bilderDpi import BilderDpi
from .bilderAmeta import BildersAmeta
from .bildersDmeta import BildersDmeta

from engine.package import FileManagerPkg
from pathlib import Path

pathModile = lambda app, end='': f"../../../../modules/{app}" + end

async def createFile():
    listApp = await FileManagerPkg.ReadFile("../../../../project.yaml")
    for app in listApp['modules']:
        pathClass = pathModile(app, '/schemas')
        if await FileManagerPkg.Exists(pathClass):
            for cl in await FileManagerPkg.GetFoldersList(pathClass):
                lFiles = await FileManagerPkg.getFilesWithExtension(f'{pathClass}/{cl}', '.odb.json')
                for File in lFiles:
                    data = await FileManagerPkg.ReadFile(File.__str__())
                    pathPyFile = pathModile(app, f"/object/{cl}")
                    await BilderDpi(data).createFileD(pathPyFile)
                    await BilderDvi(data).createFileD(pathPyFile)
                    await BilderApi(data).createFileA(pathPyFile)
                    await BilderAvi(data).createFileA(pathPyFile)

                    pathMetaFile = f'{pathClass}/{cl}'
                    await BildersDmeta(data).createFile(pathMetaFile)
                    await BildersAmeta(data).createFile(pathMetaFile)

            await _getInitModule(app)

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