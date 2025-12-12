# Пользовательский файл для логики
from core.package import Core_FileManagerPkg
from .Bc_FileDpi import Bc_FileDpi, Bc_FileObj
import asyncio

class Bc_FileApi(Bc_FileDpi):
    async def findBygidSrc(self, gidSrc):
        return await self._findByAttr('gidSrc', gidSrc)

    async def insertBygidSrc(self, gidSrc, nameFile, data):
        path = f"../../../data/{gidSrc}/{nameFile}"
        await Core_FileManagerPkg.CreateFile(path, data)
        rop = await self.insert()
        rop.gidScr = gidSrc
        rop.sPath = path
        rop.sCaption = nameFile[:nameFile.rfind('.')]
        rop.sSuffix = nameFile[nameFile.rfind('.')+1:]
        await self.update(rop)
        print(f"Сохранёт файл {rop.sCaption} для источника {rop.gidScr}")

    async def getRealPath(self, id):
        rop = await self.load(id)
        if rop is not None:
            return Core_FileManagerPkg._getObjPath(rop.sPath)
