import dearpygui.dearpygui as dpg

from core.form.widgets.ReSizeLine import ReSizeLine
from core.package.Core_AsynRunPkg import asyncRun
from core.package.Core_ThreadWorkerPkg import tw

class groupByCh:
    def __init__(self, obj, isLeft:bool=False):
        self.bottomLine = None
        self.allCh = []

        self.obj = obj
        if isLeft:
            self.line = ReSizeLine(obj=obj, tagReSize=obj.selfgroup)
        self.group = dpg.add_group(show=False, label='группа для дочерних')
        if not isLeft:
            self.line = ReSizeLine(obj=obj, tagReSize=self.group)

        
    def add(self, i):
        if self.bottomLine is not None:
            dpg.show_item(self.bottomLine)
        asyncRun(i.open(self.group, self.obj.mainForm))
        self.allCh.append(i)
        self.bottomLine = ReSizeLine(obj=i, tagReSize=i.mainGroup, isHorizontal=True, par=self.group).get()
        dpg.configure_item(self.line.btn, show=True)
        tw.submit(self._calcSize)

    def _calcSize(self):
        q = True
        while q:
            if dpg.does_item_exist(self.group):
                h = dpg.get_item_rect_size(self.group)[1] 
                if h != 0:
                    q=False
                    x = h / len(self.allCh)
                    for i in self.allCh[:-1]:
                        dpg.set_item_height(i.mainForm, x)
                        i.offset_y_resize = x

