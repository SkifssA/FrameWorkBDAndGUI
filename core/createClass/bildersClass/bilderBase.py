from core.package.FileManager import FileManagerPkg

class BilderBase:
    temp = None
    suffixFile = None
    tabSpace = ' '*4

    def __init__(self, data):
        self.data = data
        self.data['nameClass'] = self.data['name']

    def _getPathAndFile(self, path):
        return f'{path}/{self.data['name']}{self.suffixFile}'
    
    async def createFileA(self, path):
        pathWhitFile = self._getPathAndFile(path)
        if not await FileManagerPkg.Exists(pathWhitFile):
            f = self.temp.format(**self.data)
            await FileManagerPkg.CreateFile(pathWhitFile, f)

    async def createFileD(self, path):
        pathWhitFile = self._getPathAndFile(path)
        f = self.temp.format(**self.data)
        await FileManagerPkg.CreateFile(pathWhitFile, f)