from dataclasses import dataclass
from enum import StrEnum

from core.dataClass.baseDataClass import Base

class typeCommit(StrEnum):
    insert = 'insert'
    update = 'update'
    delete = 'delete'
    none = 'none'

@dataclass
class EmptyObj(Base):
    id: int = None
    gid: str = None
    sHeadLine: str = None
    sMnemoCode: str = None
    typeCommit: str = typeCommit.none

    def __str__(self):
        return f"{self.__class__.__name__}#{self.id}"
