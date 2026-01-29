import dearpygui.dearpygui as dpg
import asyncio
import os
import datetime
import threading
import time

from core.package import Core_FileManagerPkg, Core_ActionDispatcher
from core.object.Core_SelectApp import Core_SelectApp

def my_recurring_function(script: tuple):
    def k(name):
        asyncio.run(Core_ActionDispatcher().action(name))
    
    while True:
        t = datetime.datetime.now()
        print(f"{t.hour}:{t.minute}:{t.second}")
        for i in script:
            h = i.nHour if i.nHour is not None else ""
            m = i.nMinute if i.nMinute is not None else ""
            s = i.nSec if i.nSec is not None else ""

            if str(t.hour) in h.split(',') or str(t.minute) in m.split(',') or str(t.second) in s.split(','):
                threading.Thread(target=k, args=(i.sNameScript, )).start()
        time.sleep(0.99)

async def mainProgram():
    from modules.bc.object.scriptscheduler.Bc_ScriptSchedulerApi import Bc_ScriptSchedulerApi
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
        threading.Thread(target=my_recurring_function, args=(data, )).start()

    dpg.set_primary_window("main_window", True)
    dpg.maximize_viewport()
    dpg.show_viewport()
    dpg.start_dearpygui()
    dpg.destroy_context()