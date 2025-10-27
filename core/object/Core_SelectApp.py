import dearpygui.dearpygui as dpg
import asyncio
from ..package import Core_FileManagerPkg

class Core_SelectApp:
    async def open(self):
        with dpg.child_window(parent='main_window', tag='select_app'):
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
        import importlib

        full_module_name = f"{module}.object.{data['nameMainScreen']}"

        try:
            dpg.delete_item("select_app")
            # Импортируем именно модуль с классом
            moduleApp = importlib.import_module(full_module_name)
            
            # Получаем класс из этого модуля
            ScreenClass = getattr(moduleApp, data['nameMainScreen'])
            
            # Проверяем, что это действительно класс
            if not isinstance(ScreenClass, type):
                raise TypeError(f"{data['nameMainScreen']} не является классом")

            # Создаём экземпляр и вызываем метод open()
            screen_instance = ScreenClass()
            asyncio.run(screen_instance.open())

        except ImportError as e:
            print(f"Не удалось импортировать модуль '{full_module_name}': {e}")
            raise
        except AttributeError as e:
            print(f"Класс '{data['nameMainScreen']}' не найден в модуле '{full_module_name}': {e}")
            raise
        except Exception as e:
            print(f"Ошибка при создании экрана: {e}")
            raise