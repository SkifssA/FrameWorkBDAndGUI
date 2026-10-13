import os
import sys

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from core.createClass import createFile, createTab, createModule
from core.sdk import ACTIONDISPATCHER
from webapp.main import runServer

if __name__ == "__main__":
    if len(sys.argv) > 1:
        args = sys.argv[1:]  # первый элемент — имя скрипта
        if args[0] == "createClass":
            createTab(args[2])
        elif args[0] == "createSours":
            createFile(args[2])
        elif args[0] == "createModule":
            createModule("sys", "система")
        elif args[0] == "launchServer":
            runServer()
    else:
        sNameTab = "Bc_MainMenuPub"
        classPub = ACTIONDISPATCHER.getModulesConfig()
        print(classPub)
