from pathlib import Path
from core.package.FileManager import FileManagerPkg

def createModule(nameModule:str, captionModule:str):
    '''Создание модуля'''
    
    beginPath = f"module/{nameModule.lower()}/"
    folders = [f"{beginPath}/object"
               , f"{beginPath}/schemas"
               , f"{beginPath}/config"
               , f"{beginPath}/cache"
            ]
    for folder in folders:
        Path(FileManagerPkg.getRealPath(folder)).mkdir(parents=True, exist_ok=True)

    capNameModule = nameModule.capitalize()

    _createFile(f'{beginPath}/config/app.json',{'name': captionModule, 'nameMainScreen': f'{capNameModule}_MainMenu'})
    _createFile(f'{beginPath}/config/hooks.json',{})

    _createFile(f'{beginPath}/__init__.py', '')
    _createFile(f'{beginPath}/README.md', '# Модуль "{captionModule}"({nameModule})'.format(captionModule=captionModule, nameModule=capNameModule))
    _createFile(f'{beginPath}/object/{capNameModule}_MainMenuPub.py',
                """from core.sdk import Oper

class {nameModule}_MainMenuPub:
    class Default(EmptyPub.MainMenu): pass""".format(nameModule=capNameModule))
    _createFile(f'{beginPath}/cache/meta.json', {})

def _createFile(path, fileData):
    FileManagerPkg.CreateFile(path, fileData)