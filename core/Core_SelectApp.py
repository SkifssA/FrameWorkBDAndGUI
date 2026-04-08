import dearpygui.dearpygui as dpg

from core.package import Core_FileManagerPkg, Core_ActionDispatcher, Core_AsynRunPkg

class Core_SelectApp:
    async def open(self):
        with dpg.child_window(parent='main_window', tag='select_app') as mainMenuApp:
            self.mainMenuApp = mainMenuApp
            listApp = await Core_FileManagerPkg.ReadFile("../project.yaml")
            for app in listApp['modules']:
                if await Core_FileManagerPkg.Exists(f"../modules/{app}/config/app.json"):
                    data = await Core_FileManagerPkg.ReadFile(f"../modules/{app}/config/app.json")
                    self.createBlocApp(data)

    def createBlocApp(self, data):
         with dpg.child_window(
                width=-1,
                height=150,
                border=True,               # ← Включает рамку
                no_scrollbar=True
            ):
                dpg.add_text(data['name'])
                dpg.add_button(label='Открыть', callback=lambda: self.openMainMenuModule(data))

    def openMainMenuModule(self, data):
        module_name = f"{data['nameMainScreen']}.default"
        dpg.delete_item(self.mainMenuApp)
        Core_AsynRunPkg.asyncRun(Core_ActionDispatcher().action(module_name).open(parent='main_window'))

        