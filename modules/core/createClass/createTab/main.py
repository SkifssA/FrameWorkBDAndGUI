from engine.package import FileManagerPkg
from engine.package.AsynRunPkg import asyncRun

from modules.core.createClass.createTab.class_for_tab import Tab

async def createTab():
    listModules = asyncRun(FileManagerPkg.ReadFile("../project.yaml"))
    listModulesWithDep = getListModulesWithDep(listModules['modules'])
    script = []
    for app in listModulesWithDep:
        print(app)
        pathMod = f"../modules/{app}/schemas"
        lDirModSchemas = asyncRun(FileManagerPkg.GetFoldersList(pathMod, 3))
        for i in lDirModSchemas:
            w = asyncRun(FileManagerPkg.getFilesWithExtension(f"../{pathMod}/{i}", '.odb.json', 1))
            t = Tab(**asyncRun(FileManagerPkg.ReadFile(w[-1].__str__())))
            print(t)

def getListModulesWithDep(listModules: list)->list:
    listModulesWithDep = []

    for modul in listModules:
        if modul not in listModulesWithDep:
            pathClass = f"../modules/{modul}/config/app.json"
            configMod = asyncRun(FileManagerPkg.ReadFile(pathClass))
            dep = configMod.get("dependenceModules", None)
            for i in dep or []:
                if i not in listModulesWithDep:
                    w = getListModulesWithDep([i])
                    listModulesWithDep += w
            listModulesWithDep.append(modul)
    return listModulesWithDep


