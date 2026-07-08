from infi.systray import SysTrayIcon
import threading
import subprocess
import sys
import os
# Добавляем текущую директорию в путь поиска модулей
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from engine.package.AsynRunPkg import asyncRun
from engine.package import FileManagerPkg
from engine.package.ActionDispatcherPkg import ActionDispatcherPkg

from engine.Run import mainProgram

PYTHON_PATH = '.\\python\\pythonw.exe'
SUBPROCESS_DICT = {}

def openSubProcces(pathFile):
    global SUBPROCESS_DICT
    def w (x):
        if SUBPROCESS_DICT.get(pathFile, None) is None:
            SUBPROCESS_DICT[pathFile] = subprocess.Popen(
                ["cmd.exe", "/c", PYTHON_PATH, "-X", "utf8", pathFile],
                creationflags=subprocess.CREATE_NEW_CONSOLE
            )
    def wTest(x):
         threading.Thread(target=mainProgram).start()
    return wTest

def subpocPoper(nameSubProc:str, pathFile:str):
        return (nameSubProc, None, openSubProcces(pathFile))


def on_quit(x):
    for value in SUBPROCESS_DICT.values():
         value.terminate()

if __name__ == "__main__":
    conf = asyncRun(FileManagerPkg.ReadFile('../engine/config/config.json'))
    if (conf['isScriptScheduler']):
        scriptScheduler = ActionDispatcherPkg().action("Bc_ScriptSchedulerPkg.run", classMethod=True)
    
    menu_options = (
        subpocPoper('Open GUI', f"./engine/Run.py"),
        # Можно добавить другие пункты, например:
        # ("Настройки", None, lambda: print("Настройки")),
    )

    # Создаем иконку в трее
    systray = SysTrayIcon("app.ico", "TEST", menu_options=menu_options, on_quit=on_quit)
    systray.start()