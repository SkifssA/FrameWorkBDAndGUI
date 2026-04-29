import os
import sys
import asyncio
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from engine import mainProgram
from modules.core.createClass.createTab.createTab import test

if __name__ == "__main__":
    args = sys.argv[1:]  # первый элемент — имя скрипта
    test()
    # if (args[0] == 'createClass'):
    #     asyncio.run(createTab())
    # elif (args[0] == 'createSours'):
    #     asyncio.run(createFile())
    # elif (args[0] == 'launchApp'):
    #     asyncio.run(mainProgram())