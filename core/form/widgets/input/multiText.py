import dearpygui.dearpygui as dpg
import textwrap

from core.form.widgets.input.base import Base

class multiText(Base):
    def _create(self):
        self.p = self._createLable(isHorizontal=False, height=-1)
        w = dpg.add_input_text(width=-1, height=-1, on_enter=True, multiline=True, parent=self.p)
        dpg.bind_item_handler_registry(w, self._regHandler())
        return w
    
    def _get_value(self):
        return dpg.get_value(self.input)

    def _set_value(self, value):
        dpg.set_item_user_data(self.input, value if value is not None else '')
        if value is not None:
            self._on_resize('', self.input)

    def _on_resize(self, sender, app_data):
        w = dpg.get_item_rect_size(app_data)[0] // (dpg.get_text_size('d')[0])
        text:str = dpg.get_item_user_data(app_data)
        dpg.set_value(self.input, textwrap.fill(text or '', width=int(w) if w > 0 else 1))

    def _regHandler(self):
        with dpg.item_handler_registry() as w:
            dpg.add_item_resize_handler(callback=self._on_resize)
        return w

    value = property(
        fget=_get_value
        ,fset=_set_value
        )
        
        