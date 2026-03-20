from abc import ABC, abstractmethod
from typing import Any, Optional

from ..base.api import BaseApi

class AbstractForm(ABC): 
    @abstractmethod
    def thisApi(self)->BaseApi: pass

    @abstractmethod
    def onRefresh(self)->str: pass

    @abstractmethod
    def onRefreshExt(self)->str: pass

    @abstractmethod
    def getAttr(self)->Optional[Any]: pass

    @abstractmethod
    def _getAttr(self)->Optional[Any]: pass

    @abstractmethod
    def createMainForm(self, par)->int|str: pass

    @abstractmethod
    def _refresh(self, isUpdate:bool=True): pass

    @abstractmethod
    def validateClass(self): pass