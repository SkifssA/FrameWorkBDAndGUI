# Пользовательский файл для логики
from .Hbc_LessonDpi import Hbc_LessonDpi, Hbc_LessonObj
from engine.package import ASQL

class Hbc_LessonApi(Hbc_LessonDpi):

    async def findByIdExit(self, spIdExit:str)->int|None:
        return await self._findByAttr('sIdExit', spIdExit)
    
    async def getByIdExit(self, spIdExit:str)->int|None:
        id = await self._findByAttr('sIdExit', spIdExit)
        rop = await self.load(id)
        return rop

    async def register(self, spIdExit:str, spName:str)->int:
        id = await self.findByIdExit(spIdExit)
        if id is None:
            rop = await self.insert()
            rop.sCaption = spName
            rop.sIdExit = spIdExit
            await self.update(rop)
            id = rop.id
        return id
