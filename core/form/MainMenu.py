import inspect
from collections import defaultdict
import dearpygui.dearpygui as dpg
from core.base.oper import SetOper
from core.Core_SelectApp import Core_SelectApp
from core.form.Base import Base
from core.base.avi import BaseAvi
from core.package.Core_AsynRunPkg import asyncRun
from core.fabric.Form import FormConstruct

def make_btn():
    return defaultdict(lambda: {"child": defaultdict(dict)})

def to_dict(d):
    if isinstance(d, defaultdict):
        d = dict(d)
    for key, value in d.items():
        if isinstance(value, defaultdict):
            d[key] = to_dict(value)
        elif isinstance(value, dict):  # на случай обычных dict внутри
            d[key] = to_dict(value)
    return d

class mainMenu(BaseAvi):

    class Default(Base):
        @SetOper(label="Приложение", order=-10)
        def mm_main_oper(self): pass

        @SetOper(label='Выйти', headOper='mm_main_oper', order=10000)
        async def exit(self): 
            dpg.delete_item(self.parent, children_only=True)
            await Core_SelectApp().open()

        def _getAttr(self):pass
        async def _refresh(self):pass
        def getAttr(self):pass
        def onRefresh(self):pass
        def onRefreshExt(self):pass
        def thisApi(self):pass

        def createMainForm(self, par):
            w = self._createMenu()
            with dpg.menu_bar(parent=self.tab):
                for i in sorted(w, key=lambda x: w[x]['data'][1]._order):
                    with dpg.menu(label=w[i]['data'][1]._oper_label):
                        for j in sorted(w[i]['child'], key=lambda x: w[i]['child'][x]['data'][1]._order):
                            s = w[i]['child'][j]
                            dpg.add_menu_item(label=s['data'][1]._oper_label, callback=s['data'][-1])
            with dpg.child_window(parent=par) as g:
                 dpg.add_tab_bar(tag="tab_bar")
            if self.firstFrame() is not None:
                self.firstFrame().open()
            return g
            
        def firstFrame(self): pass

        def _createMenu(self):
            menuDict = make_btn()
            for name, obj in inspect.getmembers(self.__class__, predicate=inspect.isfunction):
                if hasattr(obj, '_is_oper_handler'):
                    if obj._headOper:
                        menuDict[obj._headOper]['child'][obj._oper_id]['data'] = (name, obj, self.appendAction(obj, name))
                    else:
                        menuDict[obj._oper_id]['data'] = (name, obj, self.appendAction(obj, name))
            return to_dict(menuDict)
            
    def default(self)->FormConstruct:
        return FormConstruct(self.__class__.Default)