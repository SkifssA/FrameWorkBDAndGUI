import dearpygui.dearpygui as dpg
from core.object.Core_SelectApp import Core_SelectApp 
from core.package.Core_FileManagerPkg import Core_FileManagerPkg
import os

from ..object.Core_SelectApp import Core_SelectApp

async def mainProgram():
    dpg.create_context()

    # Путь к шрифту
    font_path = Core_FileManagerPkg._getObjPath("../font/minecraft_0.ttf", index=1)
    font_path = font_path['real_path']
    if not os.path.exists(font_path):
        raise FileNotFoundError(f"Шрифт не найден: {font_path}")

    # Создаём реестр шрифтов и загружаем шрифт с кириллицей
    with dpg.font_registry():
        with dpg.font(font_path, 14) as font:
            dpg.add_font_range_hint(dpg.mvFontRangeHint_Cyrillic)

    # Устанавливаем шрифт как активный (заменяет устаревший default_font=True)
    dpg.bind_font(font)
    with dpg.window(label="Главное окно", tag="main_window", menubar=True):
        pass
    await Core_SelectApp().open()

    # Создаём viewport и запускаем
    dpg.create_viewport(title='Dear PyGui Таблица', width=800, height=600)
    dpg.setup_dearpygui()
    dpg.set_primary_window("main_window", True)
    dpg.maximize_viewport()
    dpg.show_viewport()
    dpg.start_dearpygui()
    dpg.destroy_context()