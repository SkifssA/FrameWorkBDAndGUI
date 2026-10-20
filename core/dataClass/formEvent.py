from enum import StrEnum
from dataclasses import dataclass, asdict, field
import json

class typeEvent(StrEnum):
    refresh = 'refresh'
    openForm = 'openForm'
    closeForm = 'closeForm'
    openFormLookUp = 'openFormLookUp'
    openApp = 'openApp'
    closeApp = 'closeApp'

@dataclass
class formEvent:
    type: str
    form: str
    session_id: str
    formObject: object | None = None
    personType: str = field(init=False)

    def __post_init__(self):
        if self.type == typeEvent.refresh:
            self.personType = f"{self.type}:{self.form}" 
        else:
            self.personType = self.type

    def to_json(self) -> str:
        return json.dumps(asdict(self))

    