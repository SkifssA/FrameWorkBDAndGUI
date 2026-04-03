import dearpygui.dearpygui as dpg

from core.form.widgets.input.base import Base

class multiText(Base):
    def _create(self):
        p = self._createLable(isHorizontal=False)
        return dpg.add_input_text(width=-1, height=-1, on_enter=True, multiline=True, parent=p)
        
        