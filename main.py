import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from core.sdk import validateConfig, setup_logging

if __name__ == "__main__":
    if len(sys.argv) > 1:
        setup_logging()
        args = sys.argv[1:]  # первый элемент — имя скрипта
        if args[0] == "createClass":
            from core.createClass import createTab
            validateConfig()
            createTab(args[2])
        elif args[0] == "createSources":
            from core.createClass import createFile
            validateConfig()
            createFile(args[2])
        elif args[0] == "createModule":
            from core.createClass import createModule
            validateConfig()
            createModule("sys", "система")
        elif args[0] == "launchServer":
            from webapp.main import runServer
            validateConfig()
            runServer()
    else:    
        print("Команда не найдена")