import dearpygui.dearpygui as dpg
from ..package import ASQL
from .BaseForm import BaseForm

class EmptyCard(BaseForm):
    def __init__(self):
        super().__init__()
        self.tagInput = {}

    def createMainForm(self, par):
        self.sizeBefore = self.getMaxHeightTitle()
        with dpg.group(parent=par) as group:
            for i in self.meta['attr']:
                self.createGroupInput(i)
        return group
    
    def getMaxHeightTitle(self):
        w = 0
        for i in self.meta['attr']:
            if w < len(self.meta['attr'][i]['caption']):
                w = len(self.meta['attr'][i]['caption'])
        return w * 11

    def createGroupInput(self, nameAttr:str):
        dataAttr = self.meta['attr'][nameAttr]
        if dataAttr['isVisible']:
            with dpg.child_window(border=False, height=20):
                with dpg.group(horizontal=True):
                    with dpg.child_window(width=self.sizeBefore, border=False):
                        dpg.add_text(dataAttr['caption'])
                    if dataAttr['edit'] == 'edit':
                        self.tagInput[nameAttr] = dpg.add_input_text()
                    elif dataAttr['edit'] == 'check':
                        self.tagInput[nameAttr] = dpg.add_checkbox()
                    elif dataAttr['edit'] == 'lookUp':
                        self.tagInput[nameAttr] = dpg.add_combo()