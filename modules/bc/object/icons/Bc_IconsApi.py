# Пользовательский файл для логики
from .Bc_IconsDpi import Bc_IconsDpi, Bc_IconsObj

from engine.package.FileManagerPkg import FileManagerPkg

class Bc_IconsApi(Bc_IconsDpi):
    def register(self, sCode, path):
        w = self.findByMnemocode(sCode)
        if w is None:
            w = self.insert()
            self.setsCode(w, sCode)
        else:
            w = self.load(w)

        self.setsPath(w, path)
        self.update(w)

    async def dataInstall(self):
        beginPath = '../assets/img/icon/{name}.png'
        nameIcon = [
            "add"
            ,"close"
            ,"update"
            ,"delete"
            ,"open"
            ,"save"
            ,"download"
            ,"upload"
            ,"open_in_web"
            ,"add_link"
            ,"selected"
        ]
        for i, path in enumerate(beginPath.format(name=i) for i in nameIcon):
            self.register(i, str(path))
