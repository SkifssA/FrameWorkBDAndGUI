from core.package.FileManager import FileManagerPkg
from core.dataClass.tabDataClass import dbDataShema
from core.fabric.MetaInfo import MetaInfo
from core.createClass.createTab.tab_manager import TabsManager
from core.package.ModuleManagerPkg import ModuleManagerPkg


async def createTab():
    '''Создание таблиц для классов модулей (DDL из *.odb.json).'''
    listModulesWithDep = await getListModulesWithDep(ModuleManagerPkg().getNameModule())
    scripts: list[dbDataShema] = []
    for app in listModulesWithDep:
        pathMod = f"module/{app}/schemas"
        lDirModSchemas = await FileManagerPkg.GetFoldersList(pathMod, 3)
        for i in lDirModSchemas:
            odbFiles = await FileManagerPkg.getFilesWithExtension(f"{pathMod}/{i}", '.odb.json', 1)
            for odbFile in odbFiles:
                schema = MetaInfo().getMetaTab(odbFile.__str__())
                await TabsManager.execute_pending(schema)
                scripts += schema.dbData

        pkgFiles = await FileManagerPkg.getFilesWithExtension(f"{pathMod}", '.pkg.json', 1)
        for pkgFile in pkgFiles:
            schema = MetaInfo().getMetaTab(pkgFile.__str__())
            scripts += schema.dbData
    print('-' * 10 + 'Найденные скрипты данных (выполнение не реализовано)' + '-' * 10)
    for s in scripts:
        print(s)


async def getListModulesWithDep(listModules: list) -> list:
    listModulesWithDep = []

    for modul in listModules:
        if modul not in listModulesWithDep:
            pathClass = f"module/{modul}/config/app.json"
            configMod = await FileManagerPkg.ReadFile(pathClass)
            dep = configMod.get("dependenceModules", None)
            for i in dep or []:
                w = await getListModulesWithDep([i])
                listModulesWithDep += [m for m in w if m not in listModulesWithDep]
            if modul not in listModulesWithDep:
                listModulesWithDep.append(modul)
    return listModulesWithDep


if __name__ == '__main__':
    from core import asyncRun
    asyncRun(createTab())