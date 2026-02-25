import dearpygui.dearpygui as dpg
from ..package import ASQL, Core_ActionDispatcher
from .BaseForm import BaseForm
from ..base.Event import SetterEvent
import threading
import time
import asyncio

class EmptyCard(BaseForm):
    def __init__(self):
        super().__init__()
        self.tagInput = {}
        self.obj = None
        self.sizeButton = 30

    def createMainForm(self, par):
        self.sizeBefore = 100
        with dpg.child_window(parent=par) as group:
            w = dpg.add_group(horizontal=True)
            backLastLine = True
            row = [[]]
            for i in sorted(self.meta['attr'], key=lambda x: self.meta['attr'][x]['order']):
                self.createGroupInput(i, w, backLastLine)
                if self.meta['attr'][i]['isVisible']:
                    row[-1].append(self.tagInput[i]['group'])
                    isLastLine = self.meta['attr'][i].get('isLastLine', True)
                    if isLastLine:
                        w = dpg.add_group(horizontal=True)
                        row.append([])
                    backLastLine = isLastLine
        row = row[:-1]
        threading.Thread(target=self.k, args=(row, par)).start()
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
                q = dpg.get_item_rect_size(self.mainForm)[0] - 20 - 8*(r-1)
                s = q // r
                maxW = q - s * r
                for j in row:
                    p = dpg.get_item_parent(j)
                    nChild = len(dpg.get_item_children(j)[1])
                    if nChild > 2:
                        w = dpg.get_item_children(j)[1]
                        dpg.set_item_width(w[1], s - ((self.sizeButton + 40) * 3 + 10))
                    dpg.set_item_width(p, s + maxW if j == row[-1] else s)
    
    def MaxHeightTitle(self, row):
        w = 0
        r = [i[0] for i in row if i != []]
        cw = []
        for i in r:
            p = dpg.get_item_parent(i)
            cw.append(dpg.get_item_children(p)[1][0])
            l = dpg.get_item_children(cw[-1])[1][0]
            value = dpg.get_value(l) or ''
            if w < len(value):
                w = len(value)
        sizeLable = w * 11
        for i in cw:
            dpg.set_item_width(i, sizeLable)
        
    def createGroupInput(self, nameAttr:str, groupParent, selfSizeName=False):
        dataAttr = self.meta['attr'][nameAttr]
        with dpg.child_window(border=False, height=20, width=-1, show=dataAttr['isVisible'], parent=groupParent):
            with dpg.group(horizontal=True) as g:
                with dpg.child_window(width=self.sizeBefore if selfSizeName else (len(dataAttr['caption'])*11), border=False):
                    dpg.add_text(dataAttr['caption'])
                if dataAttr['edit'] == 'edit':
                    self.tagInput[nameAttr] = {'input': dpg.add_input_text(width=-1)}
                elif dataAttr['edit'] == 'check':
                    self.tagInput[nameAttr] = {'input': dpg.add_checkbox()}
                elif dataAttr['edit'] == 'lookUp':
                    self.tagInput[nameAttr] = {'input': dpg.add_combo(width=-1)}
                elif dataAttr['edit'] == 'button':
                    self.tagInput[nameAttr] = {'input': dpg.add_input_text(width=-1)}
                    dpg.add_button(label='...', parent=g, width=self.sizeButton, callback=lambda: print("Открываю выборку"))
                    dpg.add_button(label=' ^ ', parent=g, width=self.sizeButton, callback=lambda: print("Открываю карточку"))
                    dpg.add_button(label=' X ', parent=g, width=self.sizeButton, callback=lambda: print("Очищаю"))

                self.tagInput[nameAttr]['group'] = g
                self.tagInput[nameAttr]['type'] = dataAttr['edit']

    async def initInput(self):
        w = dpg.get_item_rect_size(self.mainForm)[0]
        self.data = self.thisApi()._getDataRop(self.obj)
        dpg.configure_item(self.tab, label=self.meta['caption'] if 'caption' in self.meta else self.thisApi().calcHeadLine(self.obj))
        self.data = self.data | await self.getDataExt()
        for i in self.data:
            dpg.configure_item(self.tagInput[i]['input'], callback=SetterEvent(self).getEvent(i))
            typeW = self.tagInput[i]['type']
            if typeW == "lookUp":
                await self._initLookUp(i, self.data[i])
            elif typeW == "check":
                await self._initCheck(i, self.data[i])
            elif typeW == "button":
                await self._initButton(i, self.data[i])
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
        look = await self.getSelByAttr(i, defValue)
        data = await look.getData(self.mainForm)
        dataLook = list(i['sHeadLine'] for i in data)
        dpg.configure_item(self.tagInput[i]['input'], items=dataLook)
        dpg.configure_item(self.tagInput[i]['input'], user_data=look)

    async def _initButton(self, i, defValue):
        sel = await self.getSelByAttr(i, defValue)
        w = dpg.get_item_children(self.tagInput[i]['group'])[1]
        dpg.set_item_callback(w[-3], SetterEvent(self, 'selectValue').getEvent(i))
        dpg.set_item_callback(w[-2], SetterEvent(self, 'openCard').getEvent(i))
        dpg.set_item_callback(w[-1], SetterEvent(self, 'deleteValue').getEvent(i))
        for i in w[1:]:
            dpg.set_item_user_data(i, sel)

    def www(self, sel, n):
        async def q(x): print(n, x)
        try:
            asyncio.get_running_loop()
            asyncio.create_task(sel.openModal(q))
        except:
            asyncio.run(sel.openModal(q))
        

    async def getSelByAttr(self, i, defValue, kattr={}):
        dpg.set_value(self.tagInput[i]['input'], defValue if defValue is not None else '')
        nameClass = self.meta['attr'][i]['refTab']
        nameSel = self.meta['attr'][i]['display']
        return await Core_ActionDispatcher().action(f"{nameClass}Avi.{nameSel}", kattr=kattr)

    async def _initCheck(self, i, defValue):
        dpg.set_value(self.tagInput[i]['input'], bool(defValue) if defValue is not None else False)

    async def _initAll(self, i, defValue):
        dpg.set_value(self.tagInput[i]['input'], defValue if defValue is not None else '')

    def _getAttr(self, nameAttr:str):
        return dpg.get_value(self.tagInput[nameAttr]) or self.data[nameAttr]