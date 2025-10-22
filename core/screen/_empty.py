from textual.app import Screen
from textual.containers import Horizontal, Container
from textual.widgets import Button, Checkbox, Input, Label
from textual.geometry import Offset
from textual import on
import inspect

from collections import defaultdict
from ..widgets._contextmenu import ContextMenu

# Автоматически создаёт вложенные словари
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

def SetButton(label: str = None, order:int=0, isLong:bool = False, nameMaster:str=None):
    def decorator(func):
        button_id = func.__name__
        func._is_button_handler = True
        func._button_label = label or button_id.replace('_', ' ').title()
        func._button_id = button_id
        func._is_long = isLong
        func._order = order
        func._name_master = nameMaster
        return func
    return decorator

class Empty(Screen):
    CSS="""
    #head, Horizontal {
        width: auto;
        height: auto;
    }
    """
    def __init__(self, name = None, id = None, classes = None):
        super().__init__(name, id, classes)
        self.action = {}
        self.flt = []

    def compose(self):
        with Container(id='head'):
            yield Horizontal(id='toolBar')
            yield Horizontal(id="filters")
        yield Container(id='mainScreen')

    async def on_mount(self):
        await self._createButton()
        await self._createFilter()

    @SetButton("Назад", order=100)
    def closeScreen(self):
        self.app.pop_screen()

    async def _createFilter(self):
        flt = []
        for name, obj in inspect.getmembers(self.__class__, predicate=inspect.isfunction):
            if hasattr(obj, '_is_filter_handler'):
                flt.append((name, obj))
        for name, obj in sorted(flt, key=lambda x: x[1]._order):
           await self._createFilters(obj._filter_id, obj._filter_label, obj._where, obj._typeEdit, name)

    async def _createFilters(self, id, sCaption, where, typeEdit, func):
        if not id in self.action.keys():
            self.action[id] = getattr(self, func)
            self.flt.append(where)
            containers = self.query_one("#filters", Horizontal)
            containers.mount(typeEdit(sCaption, id=id))

    async def _createButton(self):
        btn = make_btn()
        for name, obj in inspect.getmembers(self.__class__, predicate=inspect.isfunction):
            if hasattr(obj, '_is_button_handler'):
                if obj._name_master:
                    btn[obj._name_master]['child'][obj._button_id]['data'] = (name, obj)
                    self.appendAction(obj, name)
                else:
                    btn[obj._button_id]['data'] = (name, obj)
        self.btn = to_dict(btn)
        for name in sorted(self.btn, key=lambda x: self.btn[x]['data'][1]._order):
            obj = btn[name]['data'][1]
            self._createButtonTool(obj, name, btn[name]['child'])

    def _createButtonTool(self, obj, name, child=None):
        if not obj._button_id in self.action.keys():
            btn = Button(obj._button_label, id=obj._button_id, flat=True)
            if child is None or child == {}:
                self.appendAction(obj, name)
            else:
                self.action[obj._button_id] = lambda: self.show_menu(btn)
            containers = self.query_one("#toolBar", Horizontal)
            containers.mount(btn)

    def appendAction(self, obj, name):
        bound_method = getattr(self, name)
        if obj._is_long:
            self.action[obj._button_id] = self.__createRunning(bound_method)
        else:
            self.action[obj._button_id] = bound_method

    def show_menu(self, button: Button):
        b = self.query(f'#{button.id}').filter('ContextMenu')
        for i in self.query(ContextMenu):
            i.remove()
        if b:
            return
        
        btn = button
        # ✅ Правильно: используем .region
        region = btn.region  # Region(x, y, width, height)
        x = region.x
        y = region.y + region.height  # меню под кнопкой
        button.id
        menu = ContextMenu([(self.btn[button.id]['child'][i]['data'][1]._button_label, self.btn[button.id]['child'][i]['data'][1]._button_id)
                             for i in self.btn[button.id]['child']], btn.id)
        self.mount(menu)
        menu.focus()

        # Устанавливаем позицию
        menu.offset = Offset(x, y)

    @on(Checkbox.Changed)
    async def handle_checkbox_change(self, event: Checkbox.Changed) -> None:
        attr = self.action[event.checkbox.id]
        await self._goAllScript(attr)

    @on(Input.Changed)
    def handle_input_change(self, event: Input.Changed) -> None:
        self.query_one("#status", Label).update(f"Введено: {event.value}")

    @on(Button.Pressed)
    async def handle_button_press(self, event: Button.Pressed) -> None:
        attr = self.action[event.button.id]
        await self._goAllScript(attr)
    
    async def _goAllScript(self, attr):
        if inspect.iscoroutinefunction(attr):
            # Это async def метод → вызываем и ждём
            return await attr()
        elif callable(attr):
            # Обычный метод
            return attr()

    async def _refresh(self):
        pass

    def __createRunning(self, func):
        def w():
            from ..screen import RunningScreen
            self.app.push_screen(
                RunningScreen(
                    task_func=func,
                    on_done=self._refresh
                )
            )
        return w

    

    