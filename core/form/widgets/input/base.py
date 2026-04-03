import dearpygui.dearpygui as dpg

from core.base.Event import SetterEvent

class Base:
    def __init__(self, classCard, nameAttr, parent):
        self.classCard = classCard
        self.nameAttr = nameAttr
        self.data = classCard.meta['attr'][nameAttr]
        self.parent = parent
        self.input = self._create()

    def _create(self):
        p = self._createLable()
        return dpg.add_input_text(width=-1, on_enter=True, parent=p)
            
    def _createLable(self, isHorizontal:bool=True):
        with dpg.child_window(border=False, height=20, width=-1, show=self.data['isVisible'], parent=self.parent):
            with dpg.group(horizontal=isHorizontal) as g:
                with dpg.child_window(width=len(self.data['caption'])*11, border=False, height=20):
                    dpg.add_text(self.data['caption'])
        return g

    def _get_value(self):
        return dpg.get_value(self.input)

    def _set_value(self, value):
        dpg.set_value(self.input, value if value is not None else '')

    def init(self, value):
        self.value = value
        dpg.configure_item(self.input, callback=SetterEvent(self.classCard).getEvent(self.nameAttr))

    value = property(
        fget=_get_value
        ,fset=_set_value
        )