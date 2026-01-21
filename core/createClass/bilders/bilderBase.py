from ...package import Core_FileManagerPkg

class BilderBase:
    temp = None
    suffixFile = None
    tabSpace = ' '*4

    def __init__(self, data):
        self.data = data
        self.data['nameClass'] = self.data['name']

    def _getPathAndFile(self, path):
        return f'{path}/{self.data['name']}{self.suffixFile}'
    
    async def createFile(self, path):
        pathWhitFile = self._getPathAndFile(path)
        if not await Core_FileManagerPkg.Exists(pathWhitFile):
            f = self.temp.format(**self.data)
            await Core_FileManagerPkg.CreateFile(pathWhitFile, f)