import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from core.createClass import createFile, createTab, createModule
from core.package.AsynRun import asyncRun
from core.sdk import ACTIONDISPATCHER
from webapp.main import runServer

if __name__ == "__main__":
    args = sys.argv[1:]  # первый элемент — имя скрипта
    if (args[0] == 'createClass'):
        asyncRun(createTab())
    elif (args[0] == 'createSours'):
        createFile()
    elif (args[0] == 'createModule'):
        createModule('sys', 'система')
    elif (args[0] == 'launchAppQT'):
        sNameTab = 'Bc_TimeLinePub'
        form = ACTIONDISPATCHER.getClassByName(f'{sNameTab}')
        if form:
            print('form.List().getData():\n', form.List().getData())
            print('form.List().getInfoMeta():\n', form.List().getInfoMeta())
            print('\n\n\n\n')
        runServer()