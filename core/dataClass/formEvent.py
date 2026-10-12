from enum import StrEnum
from dataclasses import dataclass

class typeEvent(StrEnum):
    refresh = 'refresh'
    openForm = 'openForm'
    openFormLookUp = 'openFormLookUp'

@dataclass
class formEvent:
    type: str
    form: str