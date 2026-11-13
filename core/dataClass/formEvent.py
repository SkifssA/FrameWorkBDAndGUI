from dataclasses import dataclass, asdict, field
import json

from core.dataClass.type import typeEvent

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

    