from typing import Any

from dataclasses import dataclass
@dataclass
class PutData:
    name_template: str
    caption_form: str
    context: dict[str, Any]