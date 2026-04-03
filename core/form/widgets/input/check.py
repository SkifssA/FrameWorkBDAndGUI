import dearpygui.dearpygui as dpg

from core.form.widgets.input.base import Base

class Check(Base):
    def _create(self):
        p = self._createLable()
        return dpg.add_checkbox(parent=p)
    
    def _get_value(self):
        return dpg.get_value(self.input)

    def _set_value(self, value):
        dpg.set_value(self.input, bool(value) if value is not None else False)

    value = property(
        fget=_get_value
        ,fset=_set_value
        )