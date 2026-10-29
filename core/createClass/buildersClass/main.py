from pathlib import Path
import re
import logging

from .builderLogic import builderLogic
from .builderPub import builderPub
from .builderDvi import builderDvi
from .builderDpi import builderDpi
from .builderAmeta import buildersAmeta
from .buildersDmeta import buildersDmeta

from core.package.FileManager import FileManagerPkg
from core.package.ModuleManagerPkg import ModuleManagerPkg
from core.fabric.MetaInfo import MetaInfo

in_core = False

pathModile = lambda app, end="": f"{'core/' if in_core else ''}module/{app}" + end

logger = logging.getLogger(__name__)

def createFile(sPath: str):
    """Создание файлов для класса"""
    global in_core
    if 'core' in sPath:
        in_core = True

    lFiles = FileManagerPkg.getFilesWithExtension(sPath, ".odb.json")
    apps = [] 
    for File in lFiles:
        app, dirName, cl = re.findall(r"module/(\w+)/\w+/(\w+)/([^.]+)", File.as_uri())[
            0
        ]

        apps.append(app)
        print(f"Обрабатывается класс {dirName}")
        module = ModuleManagerPkg()._getModule(app)
        try:
            metaFile = getattr(module, "META_FILE")
        except AttributeError:
            metaFile = {}

        print("Запись .py файлов")
        data = MetaInfo().getMetaTab(File.__str__())
        pathPyFile = pathModile(app, f"/object/{dirName}")
        builderDpi(data).createFileD(pathPyFile)
        builderDvi(data).createFileD(pathPyFile)
        builderLogic(data).createFileA(pathPyFile)
        builderPub(data).createFileA(pathPyFile)

        print("Запись .json файлов")
        pathMetaFile = pathModile(app, f"/schemas/{dirName}")
        buildersDmeta(data).createFile(pathMetaFile)
        buildersAmeta(data).createFile(pathMetaFile)

    for app in set(apps):
        lFiles = FileManagerPkg.getFilesWithExtension(pathModile(app), ".Ameta.json") + \
            FileManagerPkg.getFilesWithExtension(pathModile(app), ".Dmeta.json")
        metaFile = {i.as_uri()[i.as_uri().rfind('/')+1:]: i.as_uri()[i.as_uri().rfind('module'):] for i in lFiles}
        FileManagerPkg.CreateFile(pathModile(app, "/cache/meta.json"), metaFile)
        _getInitModule(app)


def _getInitModule(app):
    dir = pathModile(app, "/object")
    w = FileManagerPkg.getFilesWithExtension(dir, ".py")
    paths = [f for f in w if not (f.stem.endswith("Dvi") or f.stem.endswith("Dpi"))]
    base_path = Path(FileManagerPkg._getObjPath(pathModile(app))["real_path"])
    imports = []
    classLogic = []
    for p in paths:
        # Относительный путь от base_path (без расширения .py)
        rel_path = p.relative_to(base_path).with_suffix("")
        # Преобразуем в строку и заменяем '/' или '\' на '.'
        module_path = str(rel_path).replace("/", ".").replace("\\", ".")
        # Имя класса — последняя часть имени файла
        class_name = p.stem  # то же, что и rel_path.name
        # Формируем строку импорта
        import_line = f"from .{module_path} import {class_name}"
        classLogic.append(f"'{class_name}'")
        imports.append(import_line)

    FileManagerPkg.CreateFile(
        pathModile(app, "/__init__.py"),
        "\n".join(imports)
        + f"\n\nfrom core.sdk import FileManagerPkg\nMETA_FILE = FileManagerPkg.ReadFile('{pathModile(app, '/cache/meta.json')}')"
        + f"\n\n__all__ = [\n    {'\n    ,'.join(classLogic)}\n]",
    )
