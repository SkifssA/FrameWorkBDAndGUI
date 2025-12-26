import dearpygui.dearpygui as dpg
import inspect
import asyncio
from ..package.Core_FileManagerPkg import Core_FileManagerPkg
from ..base.BaseSelection import Selection

class BaseForm:
    def __init__(self):
        self.sizeLineResize = 5
        self.defaultHeight = 300

        self.last_mouse_pos = [0.0, 0.0]
        self.dragging_resize = False
        self.offset_x_resize = 0.0
        self.offset_y_resize = 0.0
        self.tab = None
        self.parent = None
        self.parentTable = None
        self.ch = None
        self.isMod = False
        self.isInsert = False

    def getTag(self):
        '''формирование тега формы'''
        return self.thisApi()._getNameClass() + str(self.parent)
        
    async def open(self, parent='tab_bar', parentTable=None):
        '''Открытие выборки'''
        self.parent = parent
        self.parentTable = parentTable
        self.ch = tuple(self.openCh())
        self.meta = await self.getMeta()
        if self.tab is not None:
            await self.refresh()
        else:    
            await self.createTab(parent, self.getW())
            self.selection = Selection(self.selfgroup)
            await self._refresh()
            await self._openCh()
        dpg.show_item(self.tab)
        dpg.set_value(parent, self.tab)
        dpg.show_item(parent)
        
            
    async def getMeta(self):
        mod, clas = self.thisApi()._getNameClass().split("_")
        path = f"../../{mod.lower()}/schemas/{clas.lower()}/{self.thisApi()._getNameClass()}"
        w = await Core_FileManagerPkg.ReadFile(f"{path}.Ameta.json")
        if (self.__class__.__name__ in w):
            return w[self.__class__.__name__]
        else:
            w = await Core_FileManagerPkg.ReadFile(f"{path}.Dmeta.json")
            return w['Default']

    def getW(self):
        '''Получение ширины'''
        w = -1
        for i in self.ch:
            if i is not None:
                if hasattr(i, 'right'):
                    if i.right:
                        w = dpg.get_viewport_width() * 0.5   
        return w
    
    async def refreshCh(self):
        '''Обновление дочерних форм'''
        for i in self.ch:
            if i is not None:
                await i.refresh()

    def openCh(self):
        '''Открытие дочерних форм. Пользовательский'''
        yield 

    async def _openCh(self):
        '''Открытие дочерних форм. Системный'''
        for i in self.ch:
            if i is not None:
                if hasattr(i, 'right'):
                    await i.open(self.rightGroup, parentTable=self.mainForm)
                    dpg.configure_item(self.LeftRight, show=True)
                else:
                    await i.open(self.tabBar, parentTable=self.mainForm)
                    dpg.configure_item(self.tabBar, show=True)
                    dpg.configure_item(self.UpDown, show=True)
                    dpg.configure_item(self.mainForm, height=self.defaultHeight)

    async def createTab(self, parent='tab_bar', width=0):
        '''Создание фрейма'''
        if (dpg.get_item_type(parent) == "mvAppItemType::mvTabBar"):
            self.tab = dpg.add_tab(label=self.meta['caption'], parent=parent, show=False)
        else:
            self.tab = parent

        with dpg.group(parent=self.tab, horizontal=True) as rightGroup:
            with dpg.group() as mainGroup: pass
            self.LeftRight = dpg.add_button(label="", width=self.sizeLineResize, height=-1, show=False)

        self.rightGroup = rightGroup
        self.selfgroup = mainGroup

        await self.createTable(mainGroup, width)

        self.regHandler()
    
    async def createTable(self, par, width=-1, height=None):
        '''Создание основного фрейма'''
        height = height if height is not None else self.defaultHeight

        with dpg.child_window(show=False, parent=par, height=40) as upToolBar:
            self.upToolBar = upToolBar
            self.toolBar = dpg.add_group(show=False, horizontal=True, tag=f'{par}_ToolBar')
        self.mainForm = self.createMainForm(par)
        self.UpDown = dpg.add_button(label="", height=self.sizeLineResize, width=width, parent=par, show=False)
        self.tabBar = dpg.add_tab_bar(show=False, parent=par)

        await self.afterCreate()

        await self.addTools()

        dpg.configure_item(self.upToolBar, show=self.meta['isVisibleToolBar'])

        dpg.configure_item(par, width=width)
        self.offset_x_resize = width
        self.offset_y_resize = height

    def createMainForm(self, par)->int|str: pass

    async def afterCreate(self)->None: pass 

    async def refresh(self):
        '''Обновление. Пользовательское'''
        await self._refresh()
        await self.refreshCh()

    async def _refresh(self):
        pass

    def regHandler(self):
        """Регистрация обработчиков и событий"""
        def on_mouse_drag(sender, app_data):
            mouse_x, mouse_y = dpg.get_mouse_pos(local=False)
            if self.dragging_resize == 1:
                dx = mouse_x - self.last_mouse_pos[0]
                self.offset_x_resize += dx
                self.last_mouse_pos[0] = mouse_x
                dpg.configure_item(self.selfgroup, width=self.offset_x_resize)
            elif self.dragging_resize == 2:
                dy = mouse_y - self.last_mouse_pos[1]
                self.offset_y_resize += dy
                self.last_mouse_pos[1] = mouse_y
                dpg.configure_item(self.mainForm, height=self.offset_y_resize)

        def on_mouse_right_down(sender, app_data):
            try:
                if dpg.is_item_hovered(self.LeftRight):
                    self.dragging_resize = 1
                elif dpg.is_item_hovered(self.UpDown):
                    self.dragging_resize = 2
                self.last_mouse_pos[:] = dpg.get_mouse_pos(local=False)
            except:
                pass

        def on_mouse_right_up(sender, app_data):
            self.dragging_resize = 0

        with dpg.handler_registry():
            dpg.add_mouse_move_handler(callback=on_mouse_drag)
            dpg.add_mouse_down_handler(button=dpg.mvMouseButton_Left, callback=on_mouse_right_down)
            dpg.add_mouse_release_handler(button=dpg.mvMouseButton_Left, callback=on_mouse_right_up)

    async def addTools(self):
        '''Обработка и создание операций'''
        q = []
        for name, obj in inspect.getmembers(self.__class__, predicate=inspect.isfunction):
            if hasattr(obj, '_is_oper_handler'):
                q.append((name, obj))
            
        oper = self.meta['oper'] if 'oper' in self.meta else {}

        for i in sorted(q, key=lambda x: x[-1]._order):
            if not dpg.does_item_exist(f'{self.selfgroup}_{i[0]}'):
                dpg.add_button(tag=f'{self.selfgroup}_{i[0]}', 
                               parent=self.toolBar, label=i[-1]._oper_label, 
                               callback=self.appendAction(i[-1], i[0]),
                               show=oper[i[0]]['isVisible'] if i[0] in oper else True
                               )
                dpg.configure_item(self.toolBar, show=True)
                dpg.configure_item(self.upToolBar, show=True)

    def appendAction(self, obj, name):
        '''Создание обработчиков для операций'''
        bound_method = getattr(self, name)
        if obj._is_long:
            return self.__createRunning(bound_method)
        else:
            return lambda: asyncio.run(bound_method())

    