import os
import sys
import asyncio
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from core.createClass.createClass import createTab, createFile
from core.base.Run import mainProgram

if __name__ == "__main__":
    asyncio.run(mainProgram())
    args = sys.argv[1:]  # первый элемент — имя скрипта
    if (args[0] == 'createClass'):
        asyncio.run(createTab())
    elif (args[0] == 'createSours'):
        asyncio.run(createFile())
    elif (args[0] == 'launchApp'):
        asyncio.run(mainProgram())