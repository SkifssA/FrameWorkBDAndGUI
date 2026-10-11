from dataclasses import dataclass, field

from core.dataClass.baseDataClass import Base

@dataclass
class EmptyObj(Base):
    def __init__(self):
        self.id:int = None

    def __str__(self):
        return f'{self.__class__.__name__}#{self.id}'