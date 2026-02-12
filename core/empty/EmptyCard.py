import dearpygui.dearpygui as dpg
from ..package import ASQL, Core_ActionDispatcher
from .BaseForm import BaseForm
import threading
import time

class EmptyCard(BaseForm):
    def __init__(self):
        super().__init__()
        self.tagInput = {}
        self.obj = None

    def createMainForm(self, par):
        self.sizeBefore = 100
        with dpg.child_window(parent=par) as group:
            w = dpg.add_group(horizontal=True)
            backLastLine = True
            row = [[]]
            for i in sorted(self.meta['attr'], key=lambda x: self.meta['attr'][x]['order']):
                self.createGroupInput(i, w, backLastLine)
                if self.meta['attr'][i]['isVisible']:
                    if (self.meta['attr'][i].get('isLastLine', True)):
                        row[-1].append(self.tagInput[i])
                        w = dpg.add_group(horizontal=True)
                        row.append([])
                    else:
                        row[-1].append(self.tagInput[i])
                    backLastLine = self.meta['attr'][i].get('isLastLine', True)
        row = row[:-1]
        threading.Thread(target=self.k, args=(row, par)).start()
        dpg.set_viewport_resize_callback(lambda: self.w(row))
        return group

    def k(self, row, mainForm):
        q = True
        while q:
            if dpg.does_item_exist(mainForm):
                if dpg.get_item_rect_size(mainForm)[0] != 0:
                    q = False
                    self.w(row)
                    self.MaxHeightTitle(row)
                    time.sleep(0.5)

    def w(self, rows):
        for row in rows:
            if row != []:
                r = len(row)
                q = dpg.get_item_rect_size(self.mainForm)[0] - 20
                s = q // r
                maxW = q - s * r
                for j in row:
                    p = dpg.get_item_parent(j)
                    p = dpg.get_item_parent(p)
                    if j == row[-1]:
                        dpg.set_item_width(p, s + maxW)
                    else:
                        dpg.set_item_width(p, s)
    
    def MaxHeightTitle(self, row):
        w = 0
        r = [i[0] for i in row if i != []]
        cw = []
        for i in r:
            p = dpg.get_item_parent(i)
            cw.append(dpg.get_item_children(p)[1][0])
            l = dpg.get_item_children(cw[-1])[1][0]
            value = dpg.get_value(l)
            if w < len(value):
                w = len(value)
        sizeLable = w * 11
        for i in cw:
            dpg.set_item_width(i, sizeLable)
        
    def createGroupInput(self, nameAttr:str, groupParent, selfSizeName=False):
        dataAttr = self.meta['attr'][nameAttr]
        with dpg.child_window(border=False, height=20, width=-1, show=dataAttr['isVisible'], parent=groupParent):
            with dpg.group(horizontal=True):
                with dpg.child_window(width=self.sizeBefore if selfSizeName else (len(dataAttr['caption'])*11), border=False):
                    dpg.add_text(dataAttr['caption'])
                if dataAttr['edit'] == 'edit':
                    self.tagInput[nameAttr] = dpg.add_input_text(width=-1)
                elif dataAttr['edit'] == 'check':
                    self.tagInput[nameAttr] = dpg.add_checkbox()
                elif dataAttr['edit'] == 'lookUp':
                    self.tagInput[nameAttr] = dpg.add_combo(width=-1)

    async def initInput(self):
        w = dpg.get_item_rect_size(self.mainForm)[0]
        self.data = self.thisApi()._getDataRop(self.obj)
        dpg.configure_item(self.tab, label=self.meta['caption'] if 'caption' in self.meta else self.thisApi().calcHeadLine(self.obj))
        self.data = self.data | await self.getDataExt()
        for i in self.data:
            dpg.configure_item(self.tagInput[i], callback=getattr(self, f'set{i}', None))
            typeW = dpg.get_item_type(self.tagInput[i])
            if typeW == "mvAppItemType::mvCombo":
                await self._initLookUp(i, self.data[i])
            elif typeW == "mvAppItemType::mvCheckbox":
                await self._initCheck(i, self.data[i])
            else:
                await self._initAll(i, self.data[i])

    async def getDataExt(self):
        dataEx = await ASQL(*self.getSqlAndParam(self.onRefreshExt()))
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
        data = await look.getData(self.mainForm)
        dataLook = list(i['sHeadLine'] for i in data)
        dpg.configure_item(self.tagInput[i], items=dataLook)
        dpg.configure_item(self.tagInput[i], user_data=look)

    async def _initCheck(self, i, defValue):
        dpg.set_value(self.tagInput[i], bool(defValue) if defValue is not None else False)

    async def _initAll(self, i, defValue):
        dpg.set_value(self.tagInput[i], defValue if defValue is not None else '')

    def _getAttr(self, nameAttr:str):
        return dpg.get_value(self.tagInput[nameAttr]) or self.data[nameAttr]