import dearpygui.dearpygui as dpg
import inspect
import asyncio

class BaseModal:
    def __init__(self, message: str, on_result_callback, sYesStr: str='Да', sNolStr: str='Нет'):
        self.on_result = on_result_callback

        with dpg.window(
            modal=True,
            show=False,
            autosize=True,
            no_title_bar=False
        ) as win:
            self.tag = win
            dpg.add_text(message)
            dpg.add_separator()
            with dpg.group(horizontal=True):
                dpg.add_button(label=sYesStr, callback=self._on_ok)
                dpg.add_button(label=sNolStr, callback=self._on_cancel)
        dpg.configure_item(self.tag, show=True)

    def _on_ok(self, sender, app_data, user_data):
        dpg.configure_item(self.tag, show=False)
        self.runOnResultCallback(True)

    def _on_cancel(self, sender, app_data, user_data):
        dpg.configure_item(self.tag, show=False)
        self.runOnResultCallback(False)

    def runOnResultCallback(self, value):
        if self.on_result:
            if inspect.iscoroutinefunction(self.on_result):
                asyncio.run(self.on_result(value))