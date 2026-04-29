from engine.package import FileManagerPkg
from engine.package.AsynRunPkg import asyncRun


def create():
    listModules = asyncRun(FileManagerPkg.ReadFile("../../project.yaml"))
    listModulesWithDep = getListModulesWithDep(listModules['modules'])
    script = []
    for app in listModulesWithDep:
        pathClass = f"../../modules/{app}/schemas"

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


