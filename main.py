import os
import sys

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

if __name__ == "__main__":
    if len(sys.argv) > 1:
        args = sys.argv[1:]  # первый элемент — имя скрипта
        if args[0] == "createClass":
            from core.createClass import createTab
            createTab(args[2])
        elif args[0] == "createSources":
            from core.createClass import createFile
            createFile(args[2])
        elif args[0] == "createModule":
            from core.createClass import createModule
            createModule("sys", "система")
        elif args[0] == "launchServer":
            from webapp.main import runServer
            from core.sdk import validateConfig
            validateConfig()
            runServer()
    else:    
        print("Команда не найдена")