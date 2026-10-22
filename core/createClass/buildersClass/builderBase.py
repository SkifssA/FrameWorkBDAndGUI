from typing import Any

from core.package.FileManager import FileManagerPkg
from core.dataClass.tabDataClass import tabSchema


class builderBase:
    temp: str | None = None
    suffixFile: str | None = None
    tabSpace = " " * 4

    def __init__(self, data: tabSchema):
        self.data: tabSchema = data
        self.dictData: dict[str, Any] = {}

    def _getPathAndFile(self, path):
        return f"{path}/{self.data.name}{self.suffixFile}"

    def createFileA(self, path):
        pathWhitFile = self._getPathAndFile(path)
        if not FileManagerPkg.Exists(pathWhitFile):
            self._createFile(pathWhitFile)

    def createFileD(self, path):
        self._createFile(self._getPathAndFile(path))

    def _createFile(self, path):
        allData = self.data.getDict() | self.dictData
        f = self.temp.format(**allData)
        FileManagerPkg.CreateFile(path, f)
