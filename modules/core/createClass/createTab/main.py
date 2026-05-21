from engine.package import FileManagerPkg
from engine.package.AsynRunPkg import asyncRun
from engine.package import ASQL

from modules.core.createClass.createTab.class_for_tab import Tab
from modules.core.createClass.createTab.script_manager import ScriptsManager
from modules.core.createClass.createTab.tab_manager import TabsManager

async def createTab():
    listModules = asyncRun(FileManagerPkg.ReadFile("../project.yaml"))
    listModulesWithDep = getListModulesWithDep(listModules['modules'])
    script = []
    for app in listModulesWithDep:
        pathMod = f"../modules/{app}/schemas"
        lDirModSchemas = asyncRun(FileManagerPkg.GetFoldersList(pathMod, 3))
        if app == 'core':
            lDirModSchemas = ['class_'] + lDirModSchemas
        for i in lDirModSchemas:
            odbFiles = asyncRun(FileManagerPkg.getFilesWithExtension(f"../{pathMod}/{i}", '.odb.json', 1))
            for odbFile in odbFiles:
                tabObject = Tab(**asyncRun(FileManagerPkg.ReadFile(odbFile.__str__())))
                asyncRun(TabsManager.execute_pending(tabObject))
                if tabObject.dbData != []:
                    script.append(*tabObject.dbData)
            
        pkgFiles = asyncRun(FileManagerPkg.getFilesWithExtension(f"../{pathMod}", '.pkg.json', 1))
        for pkgFile in pkgFiles:
            pkgObject = Tab(**asyncRun(FileManagerPkg.ReadFile(pkgFile.__str__())))
            if pkgObject.dbData != []:
                script.append(*pkgObject.dbData)

    asyncRun(ScriptsManager.execute_pending(script))
            


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

if __name__ == '__main__':
    createTab()
