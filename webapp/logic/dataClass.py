import asyncio
from typing import Any

from dataclasses import dataclass, asdict, is_dataclass, fields
from core.sdk import Form

@dataclass
class Session:
    id:str
    queue: asyncio.Queue = None
    main_menu_form: Form = None
    open_form: dict[str, Form] = None
    active_form: str = None

@dataclass
class PutData:
    name_template: str
    caption_form: str
    context: dict[str, Any]