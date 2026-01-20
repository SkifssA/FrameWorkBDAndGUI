# Пользовательский файл для логики
from .Hbc_StudentLessonDpi import Hbc_StudentLessonDpi, Hbc_StudentLessonObj

class Hbc_StudentLessonApi(Hbc_StudentLessonDpi):
    async def register(self, idStudent, idLesson):
        id = await self._findByAttr('sMnemoCode', f'{idStudent} {idLesson}')
        if id is None:
            rop = await self.insert()
            rop.idStudent = idStudent
            rop.idLesson = idLesson
            await self.update(rop)
        return id
    
    async def getAllByStudent(self, idStudent)->list[Hbc_StudentLessonObj]:
        res = []
        idl = await self._findAllByAttr('idStudent', idStudent)
        if idl is not None:
            for i in idl:
                res.append(await self.load(i))
        return res
