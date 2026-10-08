from dataclasses import dataclass, field

from core.dataClass.baseDataClass import Base

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
    typeForm: str = None
    width: int = None
    height: int = None
    filter: list[filterMetaShema] = field(default_factory=list)
    attr: list[attrMetaShema] = field(default_factory=list)
    

    