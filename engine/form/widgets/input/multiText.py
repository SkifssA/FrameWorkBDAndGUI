import dearpygui.dearpygui as dpg
import textwrap

from engine.form.widgets.input.base import Base

class multiText(Base):
    def _create(self):
        self.p = self._createLable(isHorizontal=False, height=-1)
        w = dpg.add_input_text(width=-1, height=self.data.get('height',62), on_enter=True, multiline=True, parent=self.p)
        dpg.bind_item_handler_registry(w, self._regHandler())
        return w
    
    def _get_value(self):
        return dpg.get_value(self.input)

    def _set_value(self, value):
        dpg.set_item_user_data(self.input, value if value is not None else '')
        if value is not None:
            self._on_resize('', self.input)

    def _on_resize(self, sender, app_data):
        q = dpg.get_item_rect_size(app_data)
        w = dpg.get_item_rect_size(app_data)[0] // 8
        text:str = dpg.get_item_user_data(app_data)
        dpg.set_value(self.input, textwrap.fill(text or '', width=int(w) if w > 0 else 1, tabsize=1))

    def _regHandler(self):
        with dpg.item_handler_registry() as w:
            dpg.add_item_resize_handler(callback=self._on_resize)
        return w
    
    def get_char_width(char: str, font_tag=None):
        """
        Возвращает ширину символа в пикселях.
        """
        # Создаем временную метку с одним символом
        temp_text = dpg.add_text(char)
        
        # Если нужно использовать конкретный шрифт
        if font_tag:
            dpg.bind_item_font(temp_text, font_tag)
        
        # Принудительно обновляем, чтобы размер вычислился
        dpg.render_dearpygui_frame()
        
        # Получаем размер
        width = dpg.get_item_width(temp_text)
        
        # Удаляем временный виджет
        dpg.delete_item(temp_text)
        
        return width

    value = property(
        fget=_get_value
        ,fset=_set_value
        )
        
        