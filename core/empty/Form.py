import dearpygui.dearpygui as dpg
import inspect
import asyncio
import re
from ..package.Core_FileManagerPkg import Core_FileManagerPkg
from ..base.selection import Selection
from ..base.filter import Filter
from .AbstractForm import AbstractForm
from ..package.Core_ImageManagerPkg import Core_ImageManagerPkg
from ..base.modal import FormModal, LoadModal
from ..package.Core_AsynRunPkg import asyncRun

class BaseForm(AbstractForm):

    allOpenForm = {}

    def __init__(self):
        self.sizeLineResize = 5
        self.defaultHeight = -1

        self.last_mouse_pos = [0.0, 0.0]
        self.dragging_resize = False
        self.offset_x_resize = 0.0
        self.offset_y_resize = 0.0
        self.tab = None
        self.parent = None
        self.parentTable = None
        self.ch:list[BaseForm] = None
        self.isMod = False
        self.isInsert = False
        self.isModal = False
        self.callback = None
        self.returnAttr = []
        self.right = False
        self.filter = None
        self.imgManager = Core_ImageManagerPkg()
        self.modal = None
        
    def get_impl_path(self):
        """Путь к файлу, где определён класс"""
        file = inspect.getfile(self.__class__)
        w = file.find('modules')
        file = file[w:-3].replace('object', 'schemas')
        return file
        
    @classmethod
    def getAllForm(cls):
        return BaseForm.allOpenForm

    async def open(self, parent='tab_bar', parentTable=None):
        BaseForm.allOpenForm[str(self.__class__)] = self
        '''Открытие выборки'''
        self.parent = parent
        self.parentTable = parentTable
        self.ch = tuple(self.openCh())
        self.meta = await self.getMeta()
        if dpg.does_item_exist(self.tab):
            await self.refresh()
        else:    
            await self.createTab(self.parent, self.getW())
            self.selection = Selection(self.selfgroup)
            await self._refresh()
            await self._openCh()
        dpg.show_item(self.tab)
        dpg.set_value(self.parent, self.tab)

    async def _openModal(self, callback=None, returnAttr:list=['id']):
        self.returnAttr = returnAttr
        self.callback = callback
        self.isModal = True
        self.meta = await self.getMeta()
        wd = self.meta.get('width', dpg.get_viewport_width() * 0.5)
        hg = self.meta.get('height', dpg.get_viewport_height() * 0.5)
        self.modal = FormModal(wd, hg)
        await self.modal.createMainContexWithFuc(self.open)
        dpg.split_frame()
        self.modal.show()

    def openModal(self, callback=None, returnAttr:list=['id']):
        self.asyncRun(self._openModal(callback, returnAttr))

    def asyncRun(self, coroutine):
        return asyncRun(coroutine)
                
    async def getMeta(self):
        path = f'../../{self.get_impl_path()}'
        if (path.endswith('Avi')):
            path = path[:-3]
        a = await Core_FileManagerPkg.ReadFile(f"{path}.Ameta.json")
        d = await Core_FileManagerPkg.ReadFile(f"{path}.Dmeta.json")
        if self.__class__.__name__ in a and d != 'Файл не найден':
            return self.__fillByDefault(a[self.__class__.__name__], d['Default'])
        elif (self.__class__.__name__ in a):
            return a[self.__class__.__name__]
        elif 'Default' in d:
            return d['Default']
        else:
            return {'isVisibleToolBar': False}

    def __fillByDefault(self, a, d):
        self.__w(a, d, 'caption')
        self.__w(a, d, 'isVisibleToolBar')
        self.__w(a, d, 'attr')

        for i in d['attr']:
            self.__w(a['attr'], d['attr'], i)
            for j in d['attr'][i]:
                self.__w(a['attr'][i], d['attr'][i], j)
            
        return a

    def __w(self, a, d, sNAme):
        if(sNAme not in a):
            a[sNAme] = d[sNAme]

    def getW(self):
        '''Получение ширины'''
        w = -1
        wScreen = dpg.get_viewport_width()
        for i in self.ch:
            if i is not None:
                if hasattr(i, 'right'):
                    if i.right:
                        w = self.meta.get('width', wScreen * 0.5) 
        return w
    
    async def refreshCh(self):
        '''Обновление дочерних форм'''
        for i in self.ch:
            if i is not None:
                await i.refresh() 

    async def _openCh(self):
        '''Открытие дочерних форм. Системный'''
        for i in self.ch:
            if i is not None:
                if i.right:
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
            self.tab = dpg.add_tab(label=self.meta.get('caption', ''), parent=parent, show=False)
        else:
            self.tab = parent

        self.filter = Filter(self)

        with dpg.group(parent=self.tab, horizontal=True) as rightGroup:
            with dpg.group() as mainGroup: pass
            self.LeftRight = dpg.add_button(label="", width=self.sizeLineResize, height=-1, show=False)

        self.rightGroup = rightGroup
        self.selfgroup = mainGroup

        await self.createTable(mainGroup, width)

        self.regHandler()
    
    async def createTable(self, par, width=-1, height=None):
        '''Создание основного фрейма'''
        height = height or self.defaultHeight

        with dpg.child_window(show=False, parent=par, height=52) as upToolBar:
            self.upToolBar = upToolBar
            self.toolBar = dpg.add_group(show=False, horizontal=True, tag=f'{par}_ToolBar')
        self.mainForm = self.createMainForm(par)
        dpg.set_item_user_data(self.mainForm, self)
        self.UpDown = dpg.add_button(label="", height=self.sizeLineResize, parent=par, show=False)
        self.tabBar = dpg.add_tab_bar(show=False, parent=par)

        await self.afterCreate()

        if self.meta.get('isVisibleToolBar', True):
            await self.addTools()
            dpg.configure_item(self.upToolBar, show=True)

        dpg.configure_item(par, width=width)
        self.offset_x_resize = width
        self.offset_y_resize = height

    async def refresh(self):
        '''Обновление. Пользовательское'''
        await self.validateClass()
        await self._refresh()
        await self.refreshCh()

    async def validateClass(self): pass

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
            
        oper = self.meta.get('oper', {})

        for i in sorted(q, key=lambda x: x[-1]._order):
            if not dpg.does_item_exist(f'{self.selfgroup}_{i[0]}'):
                await self.addButton(
                    tag = f'{self.selfgroup}_{i[0]}',
                    objPath=i[-1].img, 
                    parent=self.toolBar, 
                    label=i[-1]._oper_label, 
                    callback=self.appendAction(i[-1], i[0]),
                    show=oper[i[0]]['isVisible'] if i[0] in oper else i[-1].isVisible
                )
                dpg.configure_item(self.toolBar, show=True)
                dpg.configure_item(self.upToolBar, show=True)

    async def addButton(self, tag, objPath, parent, label, callback, show): 
        dpg.add_image_button(
            tag = tag,
            texture_tag = await Core_ImageManagerPkg().loadFile(objPath),
            parent = parent,
            width=30,
            height=30,
            callback=callback,
            show=show
        )
        with dpg.tooltip(tag=f'{tag}_tooltip', parent=tag, show=show):
            dpg.add_text(label)

    def appendAction(self, obj, name):
        '''Создание обработчиков для операций'''
        bound_method = getattr(self, name)
        if obj._is_long:
            return lambda: LoadModal(bound_method, f'Выполнение задачи \'{obj._oper_label}\'').show()
        else:
            return lambda: asyncio.run(bound_method())

    def closeForm(self):
        BaseForm.allOpenForm.pop(str(self.__class__), None)
        dpg.delete_item(self.tab)
        if self.modal is not None:
            self.modal.hide_overlay()

    def getSqlAndParam(self, sql:str)->tuple[str, list]:
        par = [self.getAttr(i) for i in re.findall(r':([^ ]*)', sql)]
        sql = re.sub(r':[^ ]*', '?', sql)
        return (sql, par)
    
    def openCh(self):
        '''Открытие дочерних форм. Пользовательский'''
        yield

    async def afterCreate(self)->None: pass

    def checwork(self): pass