from dataclasses import dataclass, field

from core.dataClass.baseDataClass import Base


@dataclass
class attrMetaSchema(Base):
    name: str
    caption: str = None
    type: str = None
    isVisible: bool = None
    order: float = 0
    editType: str = "edit"
    refTab: str = None
    display: str = None
    attrId: str = None


@dataclass
class filterMetaSchema(Base):
    sql: str
    attr: list[attrMetaSchema] = field(default_factory=list)


@dataclass
class metaSchema(Base):
    name: str
    caption: str = None
    isVisibleToolBar: bool = True
    typeForm: str = None
    width: int = None
    height: int = None
    filter: list[filterMetaSchema] = field(default_factory=list)
    attr: list[attrMetaSchema] = field(default_factory=list)
    tabCh: list[str] = field(default_factory=list)
