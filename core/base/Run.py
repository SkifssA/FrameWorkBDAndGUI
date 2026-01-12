import dearpygui.dearpygui as dpg
from core.object.Core_SelectApp import Core_SelectApp 
from core.package.Core_FileManagerPkg import Core_FileManagerPkg
from core.package.Core_ActionDispatcherPkg import Core_ActionDispatcherPkg
import asyncio
import os

from ..object.Core_SelectApp import Core_SelectApp

def my_recurring_function(script: tuple):
    for i in script:
        asyncio.run(Core_ActionDispatcherPkg().action(i.sNameScript))
    dpg.set_frame_callback(dpg.get_frame_count()+10, lambda: my_recurring_function(script))

async def mainProgram():
    from bc.object.scriptscheduler.Bc_ScriptSchedulerApi import Bc_ScriptSchedulerApi
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
    dpg.create_viewport(title='FrameWorkBDAndGUI', width=800, height=600)
    dpg.setup_dearpygui()

    conf = await Core_FileManagerPkg.ReadFile('../config/config.json')
    if (conf['isScriptScheduler']):
        data = await Bc_ScriptSchedulerApi()._getAllByAttr('bUsed', 1) or []
        dpg.set_frame_callback(50, lambda: my_recurring_function(
            data
            ))

    dpg.set_primary_window("main_window", True)
    dpg.maximize_viewport()
    dpg.show_viewport()
    dpg.start_dearpygui()
    dpg.show_debug()
    dpg.destroy_context()