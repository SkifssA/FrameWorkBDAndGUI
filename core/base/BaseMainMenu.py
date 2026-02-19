import inspect
from collections import defaultdict
import dearpygui.dearpygui as dpg
import asyncio
from .BaseOper import SetOper
from ..object.Core_SelectApp import Core_SelectApp

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

    @SetOper(label="Приложение", order=-10)
    def mm_main_oper(self): pass


    @SetOper(label='Выйти', headOper='mm_main_oper', order=10000)
    async def exit(self): 
        dpg.delete_item("main_window", children_only=True)
        await Core_SelectApp().open()

    async def open(self):
        w = await self._createMenu()
        with dpg.menu_bar(parent='main_window'):
            for i in sorted(w, key=lambda x: w[x]['data'][1]._order):
                with dpg.menu(label=w[i]['data'][1]._oper_label):
                    for j in sorted(w[i]['child'], key=lambda x: w[i]['child'][x]['data'][1]._order):
                        s = w[i]['child'][j]
                        dpg.add_menu_item(label=s['data'][1]._oper_label, callback=s['data'][-1])
        with dpg.tab_bar(tag="tab_bar", parent='main_window'):
            pass

    async def _createMenu(self):
        menuDict = make_btn()
        for name, obj in inspect.getmembers(self.__class__, predicate=inspect.isfunction):
            if hasattr(obj, '_is_oper_handler'):
                if obj._headOper:
                    menuDict[obj._headOper]['child'][obj._oper_id]['data'] = (name, obj, self.appendAction(obj, name))
                else:
                    menuDict[obj._oper_id]['data'] = (name, obj, self.appendAction(obj, name))
        return to_dict(menuDict)
    
    def appendAction(self, obj, name):
        '''Создание обработчиков для операций'''
        from .BaseModal import LoadModal
        bound_method = getattr(self, name)
        if obj._is_long:
            return lambda: LoadModal(bound_method, f'Выполнение задачи \'{obj._oper_label}\'').show()
        else:
            return lambda: asyncio.run(bound_method())