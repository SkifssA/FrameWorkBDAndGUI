import asyncio
import time
from typing import Any

from dataclasses import dataclass, asdict, is_dataclass, fields, field
from core.sdk import Form

@dataclass
class Tab:
    """Одно открытое окно (таб) пользователя.

    Отделяет «представление окна» от глобального состояния сессии:
    каждая вкладка хранит собственную активную форму и дочерние вкладки.
    """
    tab_id: str
    form_name: str                      # имя формы в корне таба ('' = только главное меню)
    parent_tab_id: str | None = None
    child_tab_ids: list[str] = field(default_factory=list)
    active_form: str | None = None      # активная дочерняя форма внутри таба


@dataclass
class Session:
    id:str
    queue: asyncio.Queue = None
    main_menu_form: Form = None
    open_form: dict[str, Form] = None
    active_form: str = None             # DEPRECATED: используйте Tab.active_form
    tabs: dict[str, Tab] = field(default_factory=dict)
    active_tab_id: str | None = None
    last_seen: float = field(default_factory=time.time)

@dataclass
class PutData:
    name_template: str
    caption_form: str
    context: dict[str, Any]