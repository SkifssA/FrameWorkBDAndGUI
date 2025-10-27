# Пользовательский файл для логики
from .Hbc_StudentDataDpi import Hbc_StudentDataDpi, Hbc_StudentDataObj

class Hbc_StudentDataApi(Hbc_StudentDataDpi):
    async def insertByStudent(self, idStudent, sData):
        rop = await self.insert()
        rop.idStudent = idStudent
        rop.sData = sData
        await self.update(rop)
        rop

    async def register(self, idStudent, sData):
        id = await self._findByAttr('idStudent || \'/\' || sData', str(idStudent)+'/'+sData)
        if id is None:
            id = await self.insertByStudent(idStudent, sData)
        return id
