import dearpygui.dearpygui as dpg
import os
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from engine.package.AsynRunPkg import asyncRun
from engine.package import FileManagerPkg
from engine.SelectApp import SelectApp
from engine.package.ActionDispatcherPkg import ActionDispatcherPkg


def mainProgram():
    dpg.create_context()

    # Тема для корректного отображения отключённых кнопок
    with dpg.theme() as compat_theme:
        with dpg.theme_component(dpg.mvButton, enabled_state=False):
            c = (41, 41, 44, 255)
            dpg.add_theme_color(dpg.mvThemeCol_Button, c)
            dpg.add_theme_color(dpg.mvThemeCol_ButtonHovered, c)
            dpg.add_theme_color(dpg.mvThemeCol_ButtonActive, c)
            dpg.add_theme_color(dpg.mvThemeCol_Text, (180, 180, 180, 255))

    dpg.bind_theme(compat_theme)

    # Путь к шрифту
    font_path = FileManagerPkg._getObjPath("font/Farabee Straight Medium.ttf", index=1)
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
    asyncRun(SelectApp().open())

    # Создаём viewport и запускаем
    dpg.create_viewport(title='NecoTab', width=800, height=600)

    icon_path = FileManagerPkg._getObjPath("img/icon/icons8-закрыть-40.png", index=1)
    dpg.set_viewport_small_icon(icon_path['real_path'])  # 16x16 или 32x32
    dpg.set_viewport_large_icon(icon_path['real_path'])  # 128x128 или больше

    dpg.setup_dearpygui()

    conf = asyncRun(FileManagerPkg.ReadFile('../engine/config/config.json'))
    if (conf['isScriptScheduler']):
        scriptScheduler = ActionDispatcherPkg().action("Bc_ScriptSchedulerPkg.run", classMethod=True)

    dpg.set_primary_window("main_window", True)
    # dpg.maximize_viewport()
    dpg.show_viewport()
    dpg.start_dearpygui()
    
    if (conf['isScriptScheduler']):
        scriptScheduler.runMe = False
    dpg.destroy_context()

if __name__ == '__main__':
    mainProgram()