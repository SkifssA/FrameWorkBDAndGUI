import dearpygui.dearpygui as dpg
import asyncio
from ..package import Core_FileManagerPkg
from ..package import Core_ActionDispatcherPkg

class Core_SelectApp:
    async def open(self):
        with dpg.child_window(parent='main_window', tag='select_app') as mainMenuApp:
            self.mainMenuApp = mainMenuApp
            listApp = await Core_FileManagerPkg.ReadFile("../../project.yaml")
            for app in listApp['modules']:
                if await Core_FileManagerPkg.Exists(f"../../{app}/config/configApp.json"):
                    data = await Core_FileManagerPkg.ReadFile(f"../../{app}/config/configApp.json")
                    self.createBlocApp(app, data)

    def createBlocApp(self, module, data):
         with dpg.child_window(
                width=-1,
                height=150,
                border=True,               # ← Включает рамку
                no_scrollbar=True
            ):
                dpg.add_text(data['name'])
                dpg.add_button(label='Открыть', callback=lambda: self.openMainMenuModule(module, data))

    def openMainMenuModule(self, module, data):
        module_name = f"{data['nameMainScreen']}.open"
        dpg.delete_item(self.mainMenuApp)
        asyncio.run(Core_ActionDispatcherPkg().action(module_name))

        