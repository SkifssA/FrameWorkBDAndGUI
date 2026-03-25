import inspect
import flet as ft

from collections import defaultdict
from ..base.oper import SetOper
from ..Core_SelectApp import Core_SelectApp
from .FormFlet import BaseForm
from ..base.avi import BaseAvi
from core.Core_Store import store
from core.package.Core_AsynRunPkg import asyncRun
from core.empty.TabsFlet import Tabs
from core.formhandle.FornManeger import FormHandle, FornManeger

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

    class Default(BaseForm):
        @SetOper(label="Приложение", order=-10)
        def mm_main_oper(self): pass

        @SetOper(label='Выйти', headOper='mm_main_oper', order=10000)
        async def exit(self): 
            store.page.clean()
            await Core_SelectApp().open()

        def createMainForm(self):
            w = self._createMenu()
            s = []
            for i in sorted(w, key=lambda x: w[x]['data'][1]._order):
                s.append(ft.PopupMenuButton(
                    icon='menu',  # Иконка кнопки
                    content=ft.Text(w[i]['data'][1]._oper_label, size=16),  # Текст на кнопке
                    items=[
                        ft.PopupMenuItem(content=w[i]['child'][j]['data'][1]._oper_label, on_click=w[i]['child'][j]['data'][-1]) 
                            for j in sorted(w[i]['child'], key=lambda x: w[i]['child'][x]['data'][1]._order)
                        ],
                ))

            return ft.Row(controls=s)
            
        def firstFrame(self)->FormHandle: pass
        
        def atrefCreateForm(self):
            super().atrefCreateForm()
            if self.firstFrame() is not None:
                self.firstFrame().param(parent=self).open()

        def _createMenu(self):
            menuDict = make_btn()
            for name, obj in inspect.getmembers(self.__class__, predicate=inspect.isfunction):
                if hasattr(obj, '_is_oper_handler'):
                    if obj._headOper:
                        menuDict[obj._headOper]['child'][obj._oper_id]['data'] = (name, obj, self.appendAction(obj, name))
                    else:
                        menuDict[obj._oper_id]['data'] = (name, obj, self.appendAction(obj, name))
            return to_dict(menuDict)

    @classmethod
    def default(cls)->FormHandle:
        return FornManeger.register(cls.Default)