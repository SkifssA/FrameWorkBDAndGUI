import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from core.createClass import createFile, createTab, createModule

if __name__ == "__main__":
    args = sys.argv[1:]  # первый элемент — имя скрипта
    if (args[0] == 'createClass'):
        createTab()
    elif (args[0] == 'createSours'):
        createFile()
    elif (args[0] == 'createModule'):
            createModule('sys', 'система')
    elif (args[0] == 'launchAppQT'):
        pass