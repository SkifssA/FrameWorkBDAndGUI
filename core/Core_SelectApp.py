import flet as ft

from .package import Core_FileManagerPkg, Core_ActionDispatcher, asyncRun
from core.Core_Store import store

class Core_SelectApp:
    async def open(self):
        listApp = await Core_FileManagerPkg.ReadFile("../project.yaml")
        for app in listApp['modules']:
            if await Core_FileManagerPkg.Exists(f"../modules/{app}/config/app.json"):
                data = await Core_FileManagerPkg.ReadFile(f"../modules/{app}/config/app.json")
                self.createBlocApp(data)

    def createBlocApp(self, data):
        store.page.add(ft.ElevatedButton(data['name'], on_click=lambda: self.openMainMenuModule(data)))

    def openMainMenuModule(self, data):
        store.page.clean()
        module_name = f"{data['nameMainScreen']}.default"
        asyncRun(Core_ActionDispatcher().action(module_name)).param(parent=store.page).open()

        