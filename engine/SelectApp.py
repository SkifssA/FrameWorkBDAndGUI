import dearpygui.dearpygui as dpg

from engine.package import FileManagerPkg, ActionDispatcher

class SelectApp:
    async def open(self):
        self.tabBar = 'main_window'
        self.mainForm = None
        with dpg.child_window(parent='main_window', tag='select_app') as mainMenuApp:
            self.mainMenuApp = mainMenuApp
            listApp = await FileManagerPkg.ReadFile("../project.yaml")
            for app in listApp['modules']:
                if await FileManagerPkg.Exists(f"../modules/{app}/config/app.json"):
                    data = await FileManagerPkg.ReadFile(f"../modules/{app}/config/app.json")
                    if (data.get('name', None) is not None):
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
        ActionDispatcher().action(module_name).open()

        