from dataclasses import dataclass, field
from dacite import from_dict, Config

from core.package.FileManager import FileManagerPkg
from core.dataClass.baseDataClass import Base
from core.package.AsynRun import asyncRun

@dataclass
class attrMetaShema(Base):
    name: str
    caption: str = None
    type: str = None
    isVisible: bool = False
    order: float = 0
    editType: str = 'edit'
    refTab: str = None
    display: str = None
    attrId:str = None

@dataclass
class filterMetaShema(Base):
    sql: str
    attr: list[attrMetaShema] = field(default_factory=list)

@dataclass
class metaShema(Base):
    name: str
    caption: str = None
    isVisibleToolBar: bool = True
    width: int = None
    height: int = None
    filter: list[filterMetaShema] = field(default_factory=list)
    attr: list[attrMetaShema] = field(default_factory=list)
    

    