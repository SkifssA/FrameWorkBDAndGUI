from dataclasses import dataclass, field
from dacite import from_dict, Config

from core.package.FileManager import FileManagerPkg
from core.fabric.dataClass.baseDataClass import Base
from core import asyncRun

BASE_ATTR = [
    {'name': 'id', 'caption': 'id', "type": "INT", 'edit': 'edit', 'isVisible': False, 'order': -2}
]

@dataclass
class collectionsShema(Base):
    name: str
    attr: str

@dataclass
class attrShema(Base):
    name: str
    caption: str
    type: str
    isHeadLine: bool = False
    isMnemoCode: bool = False
    isVisible: bool = True
    order: int = 0
    editType: str = 'edit'
    display: str = None
    refTab: str = None

@dataclass
class tabShema(Base):
    name: str
    caption: str
    collections: list[collectionsShema] = field(default_factory=list)
    attr: list[attrShema] = field(default_factory=list)

def getDataClass(pathOdbFile: str)->tabShema:
    data = asyncRun(FileManagerPkg.ReadFile(pathOdbFile))
    attrListByData = data.get('attr', [])

    data['attr'] = list(from_dict(data_class=attrShema, data=i) for i in attrListByData)
    data['collections'] = list(from_dict(data_class=collectionsShema, data=i) for i in data.get('collections', []))

    return from_dict(data_class=tabShema, data=data)