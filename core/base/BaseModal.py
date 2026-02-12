import dearpygui.dearpygui as dpg
import inspect
import asyncio

class BaseModal:
    def __init__(self, mess: str, width: int=-1, height:int=-1):
        self.mess = mess
        self.width = width
        self.height = height
        width = dpg.get_viewport_client_width()
        height = dpg.get_viewport_client_height()
        
        # Создаём полноэкранное окно-оверлей БЕЗ modal
        with dpg.window(
            no_title_bar=True,
            no_resize=True,
            no_move=True,
            no_scrollbar=True,
            no_collapse=True,
            no_background=False,  # Включаем фон окна
            pos=(0, 0),
            width=width,
            height=height,
            autosize=False,
            show=False
        ) as win:
            self.win = win
            # Устанавливаем полупрозрачный фон через тему окна
            with dpg.theme() as overlay_theme:
                with dpg.theme_component(dpg.mvAll):
                    dpg.add_theme_color(dpg.mvThemeCol_WindowBg, (0, 0, 0, 150), category=dpg.mvThemeCat_Core)
            dpg.bind_item_theme(win, overlay_theme)

            with dpg.child_window(width=self.width, 
                                  height=self.height, 
                                  pos=(width * 0.5 - self.width//2, height * 0.5 - self.height//2),
                                  no_scrollbar=True) as w: self.tag = w
            self.createMainContex()
    
    def createMainContex(self): pass

    def hide_overlay(self):
        dpg.delete_item(self.win)

    def show(self):
        dpg.show_item(self.win)

class DialogModal(BaseModal):

    def __init__(self, mess, callback):
        super().__init__(mess, 500, 150)
        self.on_result = callback

    def createMainContex(self):
        with dpg.group(horizontal=True, parent=self.tag):
                dpg.add_text(self.mess, wrap=480)
                dpg.add_button(label="Да", width=100, pos=(10, 120), callback=self._on_ok)
                dpg.add_button(label="Нет", width=100, pos=(390 ,120), callback=self._on_cancel)

    def _on_ok(self, sender, app_data, user_data):
        self.hide_overlay()
        self.runOnResultCallback(True)

    def _on_cancel(self, sender, app_data, user_data):
        self.hide_overlay()
        self.runOnResultCallback(False)

    def runOnResultCallback(self, value):
        if self.on_result:
            if inspect.iscoroutinefunction(self.on_result):
                asyncio.run(self.on_result(value))   

class ErrorModal(BaseModal):
    def __init__(self, mess):
        super().__init__(mess, 500, 200)

    def createMainContex(self):
        with dpg.group(parent=self.tag):
            with dpg.child_window(width=480, height=150):
                dpg.add_text(self.mess, wrap=460)
            dpg.add_button(label="Подтвердить", callback=self.hide_overlay, pos=(10, 170))

class FormModal(BaseModal):
    def __init__(self, width = -1, height = -1):
        super().__init__('', width, height)

    async def createMainContexWithFuc(self, fun):
        await fun(self.tag)