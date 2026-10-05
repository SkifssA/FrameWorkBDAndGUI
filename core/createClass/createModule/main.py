from pathlib import Path
from core.package.FileManager import FileManagerPkg
from core.package.AsynRun import asyncRun

def createModule(nameModule:str, captionModule:str):
    '''Создание модуля'''
    
    beginPath = f"module/{nameModule.lower()}/"
    folders = [f"{beginPath}/object"
               , f"{beginPath}/schemas"
               , f"{beginPath}/config"
            ]
    for folder in folders:
        Path(FileManagerPkg.getRealPath(folder)).mkdir(parents=True, exist_ok=True)

    capNameModule = nameModule.capitalize()

    _createFile(f'{beginPath}/config/app.json',{'name': captionModule, 'nameMainScreen': f'{capNameModule}_MainMenu'})
    _createFile(f'{beginPath}/config/hooks.json',{})

    _createFile(f'{beginPath}/__init__.py', '')
    _createFile(f'{beginPath}/README.md', '# Модуль "{captionModule}"({nameModule})'.format(captionModule=captionModule, nameModule=capNameModule))
    _createFile(f'{beginPath}/object/{capNameModule}_MainMenuAvi.py',
                """from engineQT.sdk import EmptyAvi
from core.sdk import SetOper

class {nameModule}_MainMenuAvi:
    class Default(EmptyAvi.MainMenu): pass""".format(nameModule=capNameModule))

def _createFile(path, fileData):
    asyncRun(FileManagerPkg.CreateFile(path, fileData))