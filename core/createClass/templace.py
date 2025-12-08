Avi = """# Пользовательский файл для интерфейса
from .{nameClass}Dvi import {nameClass}Dvi

class {nameClass}Avi({nameClass}Dvi):
    class List({nameClass}Dvi.DviList):
        pass

    class LookUp({nameClass}Dvi.DviLookUp):
        pass
"""

Api = """# Пользовательский файл для логики
from .{nameClass}Dpi import {nameClass}Dpi, {nameClass}Obj

class {nameClass}Api({nameClass}Dpi):
    pass
"""

Dvi = """# Системный файл для интерфейса
from core.base import BaseAvi, Selection
from .{nameClass}Api import {nameClass}Api, {nameClass}Obj

class {nameClass}Dvi(BaseAvi):
    thisApi = {nameClass}Api
    class DviDefault(BaseAvi.DefaultDefault):
        selection = lambda self: Selection(self.getTag())
        async def onRefresh(self):
            return \"\"\"{sqlList}\"\"\"

        async def thisRop(self)->{nameClass}Obj:
            return await super().thisRop()

        def thisApi(self)->{nameClass}Api:
            return super().thisApi()

    class DviList(DviDefault, BaseAvi.DefaultList): pass

    class DviCard(DviDefault, BaseAvi.DefaultCard): pass

    class DviLookUp(BaseAvi.DefaultLookUp):
        async def onRefresh(self):
            return \"\"\"
            SELECT t.id
                  ,t.sHeadLine 
            FROM {nameClass} AS t
            \"\"\"
"""

Dpi = """# Системный файл для логики
import asyncio
from core.base import BaseApi, BaseObj, gid

class {nameClass}Obj(BaseObj):
    def __init__(self):
        self.id:int = None
        self.gid:gid = None
        self.{attr} = None

class {nameClass}Dpi(BaseApi):
    _classObj = {nameClass}Obj

    def _getNameClass(self):
        return "{nameClass}"

    def calcHeadLine(self, rop:{nameClass}Obj)->str:
        return f'{isHeadLine}'

    def calcMnemoCode(self, rop:{nameClass}Obj)->str:
        return f'{isMnemoCode}'

    async def insert(self)->{nameClass}Obj:
        return await super().insert()

    async def delete(self, rop:{nameClass}Obj)->None:
        {deleteDetails}
        return await super().delete(rop)
    
    async def update(self, rop:{nameClass}Obj)->None:
        return await super().update(rop)
    
    async def load(self, id: int)->{nameClass}Obj:
        return await super().load(id)
"""