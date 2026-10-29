from dataclasses import dataclass
from enum import StrEnum

from core.dataClass.baseDataClass import Base

class typeCommit(StrEnum):
    insert = 'insert'
    update = 'update'
    none = 'none'

@dataclass
class EmptyObj(Base):
    id: int = None
    typeCommit: str = typeCommit.none

    def __str__(self):
        return f"{self.__class__.__name__}#{self.id}"
