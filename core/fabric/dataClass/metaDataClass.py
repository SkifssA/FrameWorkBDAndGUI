from dataclasses import dataclass, field
from dacite import from_dict, Config

from core.package.FileManager import FileManagerPkg
from core.fabric.dataClass.baseDataClass import Base
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

def getDataClass(pathMetaFile: str)->dict[metaShema]:
    res = {}
    datas = asyncRun(FileManagerPkg.ReadFile(pathMetaFile))
    for data in datas:
        attrGen = lambda x: list(from_dict(data_class=attrMetaShema, data=i) for i in x.get('attr', []))
        data['attr'] = attrGen(data)
        f = []
        for filter in data.get('filter', []):
            filter['attr'] = attrGen(filter)
            f.append(from_dict(data_class=filterMetaShema, data=filter))
        data['filter'] = f

        res[data['name']] = from_dict(data_class=metaShema, data=data)

    