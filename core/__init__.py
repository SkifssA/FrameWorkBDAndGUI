from pathlib import Path
ROOT = Path(__file__).resolve().parent.parent

from .package import LazyVal, AsyncFileManager, asyncRun, MetadataManager
from .type.Gid import Gid



Metadata = MetadataManager()

__all__ = [
    'LazyVal'
    ,'FileManagerPkg'
    ,'Gid'
    ,'asyncRun'
    ,'Metadata'
    ,'ROOT'
]