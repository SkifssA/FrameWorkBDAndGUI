from ...package import Core_FileManagerPkg
from .bilderBase import BilderBase

class BildersAmeta(BilderBase):
    suffixFile = '.Ameta.json'

    async def createFile(self, path):
        pathWhitFileA = self._getPathAndFile(path)
        if not await Core_FileManagerPkg.Exists(pathWhitFileA):
            await Core_FileManagerPkg.CreateFile(pathWhitFileA, {})