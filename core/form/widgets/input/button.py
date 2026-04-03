import dearpygui.dearpygui as dpg

from core.form.widgets.input.base import Base
from core.package.Core_AsynRunPkg import asyncRun
from core.base.Event import SetterEvent

class ButtonRef(Base):
    def _create(self):
        p = self._createLable(isHorizontal=False)
        i = dpg.add_input_text(width=-1, on_enter=True, parent=p)
        dpg.add_button(label='...', width=self.sizeButton, callback=lambda: print("Открываю выборку"), parent=p)
        dpg.add_button(label=' ^ ', width=self.sizeButton, callback=lambda: print("Открываю карточку"), parent=p)
        dpg.add_button(label=' X ', width=self.sizeButton, callback=lambda: print("Очищаю"), parent=p)
        return i
    
    def init(self, value):
        super().init(value)
        sel = asyncRun(self.getSelByAttr(i, value))
        w = dpg.get_item_children(self.tagInput[i]['group'])[1]
        dpg.set_item_callback(w[-3], SetterEvent(self, 'selectValue').getEvent(i))
        dpg.set_item_callback(w[-2], SetterEvent(self, 'openCard').getEvent(i))
        dpg.set_item_callback(w[-1], SetterEvent(self, 'deleteValue').getEvent(i))
        for i in w[1:]:
            dpg.set_item_user_data(i, sel)