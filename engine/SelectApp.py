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
        def on_row_click(sender, app_data, user_data):
            self.openMainMenuModule(user_data)

        with dpg.child_window(
            width=-1, 
            height=50, 
            border=False, 
            no_scrollbar=True
        ):
            # Невидимая кнопка на всю ширину — ловит все клики
            dpg.add_button(
                label="",
                width=-1,
                height=-1,
                tag=f"btn_{data['nameMainScreen']}",
                user_data=data,
                callback=on_row_click
            )
            
            # Поверх кнопки кладём контент через same_line
            # Сначала сдвигаемся в начало child_window
            # dpg.add_image(texture_id, width=32, height=32, pos=(5, 9))
            dpg.add_text(data['name'], pos=(15, 15))

    def openMainMenuModule(self, data):
        module_name = f"{data['nameMainScreen']}.default"
        dpg.delete_item(self.mainMenuApp)
        ActionDispatcher().action(module_name)._open()

        