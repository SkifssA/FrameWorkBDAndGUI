from core.package.FileManager import FileManagerPkg
from core.dataClass.tabDataClass import dbDataShema
from core.fabric.MetaInfo import MetaInfo
from core.createClass.createTab.tab_manager import TabsManager
from core.package.AsynRun import asyncRun


def createTab(sPath: str):
    '''Создание таблиц для классов модулей (DDL из *.odb.json).'''
    scripts: list[dbDataShema] = []

    lFiles = asyncRun(FileManagerPkg.getFilesWithExtension(sPath, '.odb.json'))
    for File in lFiles:
        schema = MetaInfo().getMetaTab(File.__str__())
        asyncRun(TabsManager.execute_pending(schema))
        scripts += schema.dbData

    pkgFiles = asyncRun(FileManagerPkg.getFilesWithExtension(sPath, '.pkg.json'))
    for File in pkgFiles:
        schema = MetaInfo().getMetaTab(File.__str__())
        scripts += schema.dbData
    
    print('-' * 10 + 'Найденные скрипты данных (выполнение не реализовано)' + '-' * 10)
    for s in scripts:
        print(s)