import os
import sys
import asyncio
import flet as ft
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
print(ft.version)
from core.createClass.createClass import createTab, createFile
from core import mainProgram

if __name__ == "__main__":
    args = sys.argv[1:]  # первый элемент — имя скрипта
    if (args[0] == 'createClass'):
        asyncio.run(createTab())
    elif (args[0] == 'createSours'):
        asyncio.run(createFile())
    elif (args[0] == 'launchApp'):
        ft.run(mainProgram)