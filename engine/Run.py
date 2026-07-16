import dearpygui.dearpygui as dpg
import os
import sys
import queue
from pathlib import Path
import threading
import traceback
import pystray
from PIL import Image
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from engine.package.AsynRunPkg import asyncRun
from engine.package import FileManagerPkg
from engine.SelectApp import SelectApp
from engine.package.ActionDispatcherPkg import ActionDispatcherPkg

PATH_ICON = 'engine/assets/img/iconApp/app.ico'
NAME_APP = 'NecoTab'

cmd_queue = queue.Queue()

def theme_registry():
    # Тема для корректного отображения отключённых кнопок
    with dpg.theme() as compat_theme:
        with dpg.theme_component(dpg.mvButton, enabled_state=False):
            c = (41, 41, 44, 255)
            dpg.add_theme_color(dpg.mvThemeCol_Button, c)
            dpg.add_theme_color(dpg.mvThemeCol_ButtonHovered, c)
            dpg.add_theme_color(dpg.mvThemeCol_ButtonActive, c)
            dpg.add_theme_color(dpg.mvThemeCol_Text, (180, 180, 180, 255))

    dpg.bind_theme(compat_theme)

def font_registry():
    # Путь к шрифту
    font_path = FileManagerPkg._getObjPath("assets/font/Farabee Straight Medium.ttf", index=1)
    font_path = font_path['real_path']
    if not os.path.exists(font_path):
        raise FileNotFoundError(f"Шрифт не найден: {font_path}")

    # Создаём реестр шрифтов и загружаем шрифт с кириллицей
    with dpg.font_registry():
        with dpg.font(font_path, 14) as font:
            dpg.add_font_range_hint(dpg.mvFontRangeHint_Cyrillic)

    # Устанавливаем шрифт как активный (заменяет устаревший default_font=True)
    dpg.bind_font(font)
    with dpg.window(label="Главное окно", tag="main_window", menubar=True, no_scrollbar=True):
        pass
    
def app_register():
    
    theme_registry()

    font_registry()

    asyncRun(SelectApp().open())

    # Создаём viewport и запускаем
    dpg.create_viewport(title=NAME_APP, width=800, height=600, small_icon=PATH_ICON, large_icon=PATH_ICON)

    dpg.setup_dearpygui()

    dpg.set_primary_window("main_window", True)
    # dpg.maximize_viewport()

    dpg.show_viewport()

def init_tray():
    def tray_worker():
        menu = pystray.Menu(
            pystray.MenuItem('Открыть интерфейс', lambda icon, item: cmd_queue.put("show_gui")),
            pystray.MenuItem('Выйти', lambda icon, item: cmd_queue.put("exit")),
        )
        icon = pystray.Icon(NAME_APP, Image.open(PATH_ICON), NAME_APP, menu)
        icon.run()

    tray_thread = threading.Thread(target=tray_worker, daemon=True)
    tray_thread.start()
    return tray_thread

def init_scheduler():
    "--- Отложеные скрипты ---"
    conf = asyncRun(FileManagerPkg.ReadFile('../engine/config/config.json'))
    if (conf['isScriptScheduler']):
        scheduler_thread = ActionDispatcherPkg().action("Bc_ScriptSchedulerPkg.run", classMethod=True)
        return scheduler_thread

def mainWhile(scheduler):
    "--- Главный цикл рендеринга (ручной) ---"
    try:
        while True:
            # Обработка команд из очереди
            try:
                cmd = cmd_queue.get_nowait()
                if cmd == "show_gui":
                    # Показываем и разворачиваем окно
                    try:
                        dpg.delete_item("main_window", children_only=True)
                        asyncRun(SelectApp().open())

                        dpg.show_viewport()
                    except AttributeError:
                        # Если restore_viewport нет, просто показываем
                        dpg.configure_viewport("viewport", show=True)
                    print("Окно показано")
                elif cmd == "exit":
                    print("Выход по команде")
                    break
            except queue.Empty:
                pass

            # Рендеринг одного кадра с обработкой ошибок
            try:
                dpg.render_dearpygui_frame()
            except Exception as e:
                print(f"Ошибка рендеринга: {e}")
                traceback.print_exc()
                # Если ошибка критическая, можно выйти
                break

    except KeyboardInterrupt:
        print("Прервано пользователем")
    except Exception as e:
        print(f"Критическая ошибка: {e}")
        traceback.print_exc()
    finally:
        dpg.destroy_context()
        if scheduler:
            scheduler.runMe = False
        print("Программа завершена")

def mainProgram():
    dpg.create_context()

    scheduler = init_scheduler()

    app_register()

    init_tray()

    print("Цикл рендеринга запущен.")
    mainWhile(scheduler)

if __name__ == '__main__':
    mainProgram()