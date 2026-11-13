import asyncio
from dataclasses import dataclass, field
from typing import Optional
import time

from core.empty.pub import EmptyPub

@dataclass
class GroupedData:
    all_items: list = field(default_factory=list)
    groups: dict = field(default_factory=dict)
    
    def add_to_group(self, item, group_name):
        if item != []:
            self.all_items.extend(item)
            self.groups[group_name] = item

    def get_group(self, group_name:str)->list:
        return self.groups.get(group_name, [])

    def get_all(self):
        return self.all_items
    
@dataclass
class Session:
    id:str
    app: Optional[EmptyPub.MainMenu] = None
    _queue: Optional[asyncio.Queue] = None
    _last_access: float = time.time()
    _load_obj: GroupedData = field(default_factory=GroupedData)
    
    @property
    def queue(self):
        import uuid
        w = self._queue
        if not w:
            self._queue = w = asyncio.Queue()
            w.name = f"q-{uuid.uuid4().hex[:6]}"
        return w