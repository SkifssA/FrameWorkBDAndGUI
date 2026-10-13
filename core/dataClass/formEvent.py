from enum import StrEnum
from dataclasses import dataclass, asdict
import json

class typeEvent(StrEnum):
    refresh = 'refresh'
    openForm = 'openForm'
    openFormLookUp = 'openFormLookUp'

@dataclass
class formEvent:
    type: str
    form: str
    session_id: str

    def to_json(self) -> str:
        return json.dumps(asdict(self))