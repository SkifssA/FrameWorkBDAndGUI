import asyncio
from dataclasses import dataclass, field
from typing import Optional
import time

from core.emptySubClass.base import Base as BaseSubClass

@dataclass
class Session:
    id:str
    active_form: Optional[str] = None
    open_form: dict[str, BaseSubClass] = field(default_factory=dict)
    main_menu_form: Optional[BaseSubClass] = None
    _queue: Optional[asyncio.Queue] = None
    _last_access: float = time.time()
    _load_obj: dict = field(default_factory=dict)
    
    @property
    def queue(self):
        import uuid
        w = self._queue
        if not w:
            self._queue = w = asyncio.Queue()
            w.name = f"q-{uuid.uuid4().hex[:6]}"
        return w