import dearpygui.dearpygui as dpg
import inspect
import re
from typing import TypedDict

from engine.base.selection import Selection
from engine.base.filter import Filter
from engine.form.Abstract import Abstract
from engine.package.ImageManagerPkg import ImageManagerPkg
from engine.base.modal import FormModal, LoadModal
from engine.package.AsynRunPkg import asyncRun
from engine.package.MetadataManager import Metadata
from engine.form.widgets.groupByCh import groupByCh
from engine.form.widgets.ReSizeLine import ReSizeLine
from engine.package.FileManagerPkg import FileManagerPkg
from engine.package.LazyVal import LazyVal
from engine.package.DbManagerPkg import ASQL


class Config(TypedDict, total=False):
    locat: str
    isUpdate: bool
    isCh: bool

class Base(Abstract):

    def getImgDict():
        w = asyncRun(ASQL(
        """
        SELECT t.id,
            t.gid,
            t.sCode,
            t.sPath
        FROM Bc_Icons AS t
        """
        ))
        return {i['sCode']: i['sPath'] for i in w}

    imgDict = LazyVal(getImgDict)

    def __init__(self):
        from engine.base.rect import Rect
        from engine.fabric.Form import FormConstruct
        self.sizeLineResize = 5
        self.defaultHeight = -1

        self.offset_x_resize = 0.0
        self.offset_y_resize = 0.0
        self.tab = None
        self.parent = None
        self.parentTable = None
        self.ch:list[FormConstruct] = None
        self.isMod = False
        self.isInsert = False
        self.isModal = False
        self.callback = None
        self.returnAttr = []
        self.right = False
        self.filter = None
        self.imgManager = ImageManagerPkg()
        self.meta = Metadata.get(self)
        self.modal = None
        self.locationCh = {}
        self.rect = Rect(self)
        self.isCh = False

    async def open(self, parent='tab_bar', parentTable=None):
        '''Открытие выборки'''
        self.parent = parent
        self.parentTable = parentTable
        self.ch = tuple(self.openCh())
        if dpg.does_item_exist(self.tab):
            await self.refresh()
        else:    
            await self.createTab(self.parent, self.getW())
            self.selection = Selection(self.selfgroup)
            await self._refresh()
            await self._openCh()
        dpg.show_item(self.tab)
        dpg.set_value(self.parent, self.tab)

    def _openModal(self, callback=None, returnAttr:list=['id']):
        self.returnAttr = returnAttr
        self.callback = callback
        self.isModal = True
        wd = self.meta.get('width', dpg.get_viewport_width() * 0.5)
        hg = self.meta.get('height', dpg.get_viewport_height() * 0.5)
        self.modal = FormModal(wd, hg)
        self.modal.createMainContexWithFuc(self.open)
        self.modal.show()

    def openModal(self, callback=None, returnAttr:list=['id']):
        self._openModal(callback, returnAttr)

    def getW(self):
        '''Получение ширины'''
        w = -1
        wScreen = dpg.get_viewport_width()
        for i in self.ch:
            if i is not None:
                if hasattr(i.clsForm, 'locat'):
                    if i.clsForm.locat == 'right':
                        w = self.meta.get('width', wScreen * 0.5) 
        return w
    
    async def refreshCh(self):
        '''Обновление дочерних форм'''
        for i in self.ch:
            if i is not None:
                await i.clsForm.refresh() 

    async def _openCh(self):
        '''Открытие дочерних форм. Системный'''
        from engine.fabric.Form import Locat
        for i in self.ch:
            if i is not None:
                i.param(isCh=True)
                if i.clsForm.locat == Locat.right:
                    self.rightGroup.add(i)
                elif i.clsForm.locat == Locat.bottom:
                    i.open()
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

        with dpg.group(parent=self.tab, horizontal=True) as mainGroup:
            self.mainGroup = mainGroup
            self.leftGroup = groupByCh(self)
            self.selfgroup = dpg.add_group(label=f"Отображение класса {inspect.getfile(self.__class__)}")
            self.rightGroup = groupByCh(self, True)

        # dpg.show_item_registry()

        await self.createTable(self.selfgroup, width)
    
    async def createTable(self, par, width=-1, height=None):
        '''Создание основного фрейма'''
        height = height or self.defaultHeight

        with dpg.child_window(show=False, parent=par, height=52) as upToolBar:
            self.upToolBar = upToolBar
            self.toolBar = dpg.add_group(show=False, horizontal=True, tag=f'{par}_ToolBar')
        self.mainForm = self.createMainForm(par)
        dpg.set_item_user_data(self.mainForm, self)
        dpg.configure_item(self.mainForm, label=f"ГЛАВНАЯ ФОРМА")
        self.UpDown = ReSizeLine(self, self.mainForm, isHorizontal=True, par=par).btn
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
        self.rectUpdate()
        await self._refresh()
        await self.refreshCh()

    async def validateClass(self): pass

    async def addTools(self):
        '''Обработка и создание операций'''
        q = []
        for name, obj in inspect.getmembers(self.__class__, predicate=inspect.isfunction):
            if hasattr(obj, '_is_oper_handler'):
                q.append((name, obj))
            
        oper = self.meta.get('oper', {})

        for i in sorted(q, key=lambda x: x[-1]._order):
            if not dpg.does_item_exist(f'{self.selfgroup}_{i[0]}'):
                self.addButton(
                    tag = f'{self.selfgroup}_{i[0]}',
                    objPath=FileManagerPkg._getObjPath(self.imgDict.get(i[-1].img, ''), index=0), 
                    parent=self.toolBar, 
                    label=i[-1]._oper_label, 
                    callback=self.appendAction(i[-1], i[0]),
                    show=oper[i[0]]['isVisible'] if i[0] in oper else i[-1].isVisible,
                    enabled=True
                )
                dpg.configure_item(self.toolBar, show=True)
                dpg.configure_item(self.upToolBar, show=True)

    def addButton(self, tag, objPath, parent, label, callback, show, enabled): 
        dpg.add_image_button(
            tag = tag,
            texture_tag = asyncRun(ImageManagerPkg().loadFile(objPath)),
            parent = parent,
            width=30,
            height=30,
            callback=callback,
            show=show,
            enabled=enabled
        )
        with dpg.tooltip(tag=f'{tag}_tooltip', parent=tag, show=show):
            dpg.add_text(label)

    def appendAction(self, obj, name):
        '''Создание обработчиков для операций'''
        bound_method = getattr(self, name)
        if obj._is_long:
            return lambda: LoadModal(bound_method, f'Выполнение задачи \'{obj._oper_label}\'').show()
        else:
            return lambda: asyncRun(bound_method())

    def closeForm(self):
        dpg.delete_item(self.tab)
        if self.modal is not None:
            self.modal.hide_overlay()
    
    def rectUpdate(self):
        self.rect.refresh()

    def openCh(self):
        '''Открытие дочерних форм. Пользовательский'''
        yield

    def thisRop(self):
        return self.thisApi().load(self.rect.getData()[0].get('id', None))

    async def afterCreate(self)->None: pass

    def checwork(self): pass