import dearpygui.dearpygui as dpg
from ..package import ASQL, Core_ActionDispatcher
from .BaseForm import BaseForm
import re

class EmptyCard(BaseForm):
    def __init__(self):
        super().__init__()
        self.tagInput = {}
        self.obj = None

    def createMainForm(self, par):
        self.sizeBefore = self.getMaxHeightTitle()
        with dpg.child_window(parent=par) as group:
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
        with dpg.child_window(border=False, height=20, width=-1, show=dataAttr['isVisible']):
            with dpg.group(horizontal=True):
                with dpg.child_window(width=self.sizeBefore, border=False):
                    dpg.add_text(dataAttr['caption'])
                if dataAttr['edit'] == 'edit':
                    self.tagInput[nameAttr] = dpg.add_input_text(width=-1)
                elif dataAttr['edit'] == 'check':
                    self.tagInput[nameAttr] = dpg.add_checkbox()
                elif dataAttr['edit'] == 'lookUp':
                    self.tagInput[nameAttr] = dpg.add_combo(width=-1)

    async def initInput(self):
        self.data = self.thisApi()._getDataRop(self.obj)
        print(self.obj.__dict__.copy())
        dpg.configure_item(self.tab, label=self.meta['caption'] if 'caption' in self.meta else self.thisApi().calcHeadLine(self.obj))
        self.data = self.data | await self.getDataExt()
        for i in self.tagInput:
            dpg.configure_item(self.tagInput[i], callback=getattr(self, f'set{i}', None))
            typeW = dpg.get_item_type(self.tagInput[i])
            if typeW == "mvAppItemType::mvCombo":
                await self._initLookUp(i, self.data[i])
            elif typeW == "mvAppItemType::mvCheckbox":
                await self._initCheck(i, self.data[i])
            else:
                await self._initAll(i, self.data[i])

    async def getDataExt(self):
        nameAttrSqlExt = re.findall(r':([a-zA-Z_][a-zA-Z0-9_]*)', self.onRefreshExt())
        attraExt = {}
        for i in nameAttrSqlExt:
            attraExt[i] = self.data[i]
        dataEx = await ASQL(self.onRefreshExt(), attraExt)
        if dataEx != []:
            return dataEx[0]
        return {}

    def afterSetter(self):
        self.isMod = True
        self.checwork()

    async def _initLookUp(self, i, defValue):
        dpg.set_value(self.tagInput[i], defValue if defValue is not None else '')
        nameClass = self.meta['attr'][i]['refTab']
        nameLook = self.meta['attr'][i]['display']
        look = await Core_ActionDispatcher().action(f"{nameClass}Avi.{nameLook}")
        data = await look.getData()
        dataLook = list(i['sHeadLine'] for i in data)
        dpg.configure_item(self.tagInput[i], items=dataLook)
        dpg.configure_item(self.tagInput[i], user_data=look)

    async def _initCheck(self, i, defValue):
        dpg.set_value(self.tagInput[i], bool(defValue) if defValue is not None else False)

    async def _initAll(self, i, defValue):
        dpg.set_value(self.tagInput[i], defValue if defValue is not None else '')

    def _getAttr(self, nameAttr:str):
        return dpg.get_value(self.tagInput[nameAttr])