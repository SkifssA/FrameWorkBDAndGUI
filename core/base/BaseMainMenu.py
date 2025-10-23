import inspect
from collections import defaultdict
import dearpygui.dearpygui as dpg
import asyncio

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

class mainMenu:
    async def open(self):
        w = await self._createMenu()
        print(w)
        with dpg.window(label="Главное окно", tag="main_window", menubar=True):
            with dpg.menu_bar():
                for i in w:
                    with dpg.menu(label=w[i]['data'][1]):
                        for j in sorted(w[i]['child'], key=lambda x: w[i]['child'][x]['data'][1]._order):
                            s = w[i]['child'][j]
                            dpg.add_menu_item(label=s['data'][1]._oper_label, callback=s['data'][-1])
            with dpg.tab_bar(tag="tab_bar"):
                pass

    async def _createMenu(self):
        menuDict = make_btn()
        for name, obj in inspect.getmembers(self.__class__, predicate=inspect.isfunction):
            if hasattr(obj, '_is_oper_handler'):
                if obj._headOper:
                    menuDict[obj._headOper]['child'][obj._oper_id]['data'] = (name, obj, self.appendAction(obj, name))
                else:
                    menuDict[obj._oper_id]['data'] = (name, obj._oper_label, obj)
        return to_dict(menuDict)
    
    def appendAction(self, obj, name):
        bound_method = getattr(self, name)
        if obj._is_long:
            return self.__createRunning(bound_method)
        else:
            return lambda: asyncio.run(bound_method())