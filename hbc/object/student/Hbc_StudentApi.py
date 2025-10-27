# Пользовательский файл для логики
from .Hbc_StudentDpi import Hbc_StudentDpi, Hbc_StudentObj

class Hbc_StudentApi(Hbc_StudentDpi):

    async def findByName(self, spName:str)->int|None:
        return await self._findByAttr('sName', spName)
    
    async def findBybEnd(self)->list[int]|None:
        return await self._findAllByAttr('bEnd', None)

    async def getByName(self, spName:str):
        id = await self.findByName(spName)
        rop = await self.load(id)
        return rop

    async def register(self, spName:str, sContact:str, sIpVM:str, sLoginVM:str, sPassworVM:str)->int:
        id = await self.findByName(spName)
        if id is None:
            rop = await self.insert()
            rop.sName = spName
            rop.sContact = sContact
            rop.sIpVM = sIpVM
            rop.sLoginVM = sLoginVM
            rop.sPassworVM = sPassworVM
            await self.update(rop)
            id = rop.id
        return id
    
    async def setsIdNew(self, rop, value):
        rop.sIdNew = value
        await self.update(rop)
