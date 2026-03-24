import flet as ft

from core.Core_SelectApp import Core_SelectApp
from core.package.Core_FileManagerPkg import Core_FileManagerPkg
from core.Core_Store import store

# from modules.bc.object.Bc_ScriptSchedulerPkg import Bc_ScriptSchedulerPkg

async def mainProgram(page: ft.Page):
    page.title = "NecoTab"
    store.page = page

    # conf = await Core_FileManagerPkg.ReadFile('config/config.json')
    # if (conf['isScriptScheduler']):
    #     scriptScheduler = await Bc_ScriptSchedulerPkg.run()

    await Core_SelectApp().open()