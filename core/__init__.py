from pathlib import Path
ROOT = str(Path(__file__).resolve().parent.parent)

from core.package.FileManager import FileManagerPkg
PATHICO = FileManagerPkg.getRealPath("core/assets/img/iconApp/app.ico")

from .package import LazyVal, asyncRun, METADATA, ACTIONDISPATCHER
from .type.Gid import Gid

__all__ = [
    'ACTIONDISPATCHER'
    ,'METADATA'
    ,'ROOT'

    ,'LazyVal'
    ,'FileManagerPkg'
    ,'Gid'
    ,'asyncRun'
    ,'Metadata'
]