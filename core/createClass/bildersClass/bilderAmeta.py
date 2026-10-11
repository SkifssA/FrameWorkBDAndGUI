from core.package.FileManager import FileManagerPkg
from .bilderBase import BilderBase

class BildersAmeta(BilderBase):
    suffixFile = '.Ameta.json'
# 
    def createFile(self, path):
        pathWhitFile = self._getPathAndFile(path)
        if not FileManagerPkg.Exists(pathWhitFile):
            FileManagerPkg.CreateFile(pathWhitFile, {'dep': f'{self.data.name}.Dmeta.json'})
        return {f'{self.data.name}{self.suffixFile}': pathWhitFile}