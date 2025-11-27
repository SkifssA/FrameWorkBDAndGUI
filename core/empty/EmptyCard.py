import dearpygui.dearpygui as dpg
from ..package import ASQL
from .BaseForm import BaseForm

class EmptyCard(BaseForm):
    def createMainForm(self, par):
        print(self.meta['attr'])
        self.sizeBefore = self.getMaxHTitle()
        print(f"{self.sizeBefore=}")
        with dpg.group(parent=par) as group:
            for i in self.meta['attr']:
                self.createGroupInput(i)
        return group
    
    def getMaxHTitle(self):
        w = 0
        for i in self.meta['attr']:
            if w < len(self.meta['attr'][i]['caption']):
                w = len(self.meta['attr'][i]['caption'])
        return w

    def createGroupInput(self, nameAttr):
        dataAttr = self.meta['attr'][nameAttr]
        with dpg.group(horizontal=True) as group:
            dpg.add_text(f"{dataAttr['caption']: <self.sizeBefore}")
            dpg.add_input_text()
        pass