from core.package.FileManager import FileManagerPkg
from core.fabric.dataClass.tabDataClass import tabShema

class BilderBase:
    temp = None
    suffixFile = None
    tabSpace = ' '*4

    def __init__(self, data:tabShema):
        self.data:tabShema = data
        self.dictData = {}

    def _getPathAndFile(self, path):
        return f'{path}/{self.data.name}{self.suffixFile}'
    
    async def createFileA(self, path):
        pathWhitFile = self._getPathAndFile(path)
        if not await FileManagerPkg.Exists(pathWhitFile):
            await self._createFile(pathWhitFile)

    async def createFileD(self, path):
        await self._createFile(self._getPathAndFile(path))

    async def _createFile(self, path):
        allData = self.data.getDict() | self.dictData
        f = self.temp.format(**allData)
        await FileManagerPkg.CreateFile(path, f)