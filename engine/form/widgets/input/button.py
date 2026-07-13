import dearpygui.dearpygui as dpg

from engine.form.widgets.input.base import Base
from engine.package.AsynRunPkg import asyncRun
from engine.base.Event import SetterEvent

class ButtonRef(Base):

    sizeButton = 30

    def _create(self):
        p = self._createLable(isHorizontal=True)
        i = dpg.add_input_text(width=200, on_enter=True, parent=p)
        dpg.add_button(label='...', width=self.sizeButton, callback=lambda: print("Открываю выборку"), parent=p)
        dpg.add_button(label=' ^ ', width=self.sizeButton, callback=lambda: print("Открываю карточку"), parent=p)
        dpg.add_button(label=' X ', width=self.sizeButton, callback=lambda: print("Очищаю"), parent=p)
        return i
    
    def init(self, value):
        super().init(value)
        w = dpg.get_item_children(self.groupInput)[1]
        dpg.set_item_callback(w[-3], SetterEvent(self.classCard, 'selectValue').getEvent(self.nameAttr))
        dpg.set_item_callback(w[-2], SetterEvent(self.classCard, 'openCard').getEvent(self.nameAttr))
        dpg.set_item_callback(w[-1], SetterEvent(self.classCard, 'deleteValue').getEvent(self.nameAttr))
        for i in w[1:]:
            dpg.set_item_user_data(i, value)