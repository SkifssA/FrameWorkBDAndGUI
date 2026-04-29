import dearpygui.dearpygui as dpg

from engine.package import ActionDispatcher
from engine.package.AsynRunPkg import asyncRun
from engine.form.widgets.input.base import Base

class LookUp(Base):
    def _create(self):
        p = self._createLable()
        return dpg.add_combo(width=-1, parent=p)
    
    def init(self, value):
        super().init(value)
        look = self.getSelByAttr()
        data = asyncRun(look.getData(self.classCard.mainForm))
        dataLook = list(i['sHeadLine'] for i in data)
        dpg.configure_item(self.input, items=dataLook)
        dpg.configure_item(self.input, user_data=look)

    def getSelByAttr(self, kattr={}):
        nameClass = self.classCard.meta['attr'][self.nameAttr]['refTab']
        nameSel = self.classCard.meta['attr'][self.nameAttr]['display']
        return ActionDispatcher().action(f"{nameClass}Avi.{nameSel}", kattr=kattr)