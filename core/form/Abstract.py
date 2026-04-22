from abc import ABC, abstractmethod
from typing import Any, Optional

from core.base.api import BaseApi
from core.base.obj import BaseObj

class Abstract(ABC): 
    @abstractmethod
    def thisApi(self)->BaseApi: pass

    @abstractmethod
    def onRefresh(self)->str|list|BaseObj: pass

    @abstractmethod
    def onRefreshExt(self)->str: pass

    @abstractmethod
    def getAttr(self, name)->Optional[Any]: pass

    @abstractmethod
    def _getAttr(self, name)->Optional[Any]: pass

    @abstractmethod
    def createMainForm(self, par)->int|str: pass

    @abstractmethod
    async def _refresh(self): pass

    @abstractmethod
    async def validateClass(self): pass