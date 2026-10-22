from core.package.FileManager import FileManagerPkg
from .builderBase import builderBase


class buildersAmeta(builderBase):
    suffixFile = ".Ameta.json"

    #
    def createFile(self, path):
        pathWhitFile = self._getPathAndFile(path)
        if not FileManagerPkg.Exists(pathWhitFile):
            FileManagerPkg.CreateFile(
                pathWhitFile, {"dep": f"{self.data.name}.Dmeta.json"}
            )
