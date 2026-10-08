from core.package.FileManager import FileManagerPkg
from .bilderBase import BilderBase

class BildersAmeta(BilderBase):
    suffixFile = '.Ameta.json'
# if not await FileManagerPkg.Exists(pathWhitFileA):
    async def createFile(self, path):
        pathWhitFile = self._getPathAndFile(path)
        await FileManagerPkg.CreateFile(pathWhitFile, {'dep': f'{self.data.name}.Dmeta.json'})
        return {f'{self.data.name}{self.suffixFile}': pathWhitFile}