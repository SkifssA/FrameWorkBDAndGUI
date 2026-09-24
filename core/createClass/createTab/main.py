import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent.parent.parent))

from core.package.FileManager import FileManagerPkg
from core import asyncRun
from core.DB.Turso import ASQL

from core.createClass.createTab.class_for_tab import Tab
from core.createClass.createTab.script_manager import ScriptsManager
from core.createClass.createTab.tab_manager import TabsManager

def createTab():
    '''Создание таблиц для класса'''
    listModules = asyncRun(FileManagerPkg.ReadFile("../../project.yaml"))
    listModulesWithDep = getListModulesWithDep(listModules['modules'])
    script = []
    for app in listModulesWithDep:
        pathMod = f"../modules/{app}/schemas"
        lDirModSchemas = asyncRun(FileManagerPkg.GetFoldersList(pathMod, 3))
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
    print('-'*10 + 'Начало выполнение скриптов' + '-'*10)
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
    asyncRun(createTab())
