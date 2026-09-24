from core.package.FileManager import FileManagerPkg
from .bilderBase import BilderBase

class BildersAmeta(BilderBase):
    suffixFile = '.Ameta.json'

    async def createFile(self, path):
        pathWhitFileA = self._getPathAndFile(path)
        if not await FileManagerPkg.Exists(pathWhitFileA):
            await FileManagerPkg.CreateFile(pathWhitFileA, {})