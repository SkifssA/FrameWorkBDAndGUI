from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QLabel, QTableWidget, QTableWidgetItem, 
    QTabWidget, QGroupBox, QLineEdit, QComboBox, QCheckBox,
    QSystemTrayIcon, QMenu, QMessageBox, QSplitter, QFrame, QToolBar
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QIcon, QAction
from PyQt6.QtWidgets import QHeaderView

from typing import TypedDict
from abc import ABC, abstractmethod
from typing import Any, Optional, Generator

from core import Metadata
from core.package.Rect import Rect
from core.ui.widget.menubar import SetOper, OperUIBuilder, OperRegistry
from core.ui.widget.groupForm import GroupForm
from core.type.Event import SetterEvent

class Config(TypedDict, total=False):
    locat: str
    isUpdate: bool
    isCh: bool

class Base(QWidget):

    IsToolBar = True

    def __init__(self, **kwargs):
        super().__init__()

        for key, value in kwargs.items():
            setattr(self, key, value)

        self.registry = OperRegistry()
        self.oper = OperUIBuilder(self.registry)
        self.metaInfo = Metadata.get(self)
        self.Rect = Rect(self)
        self.formParent = None
        self.caption = self.metaInfo.get('caption', 'НАЗВАНИЯ НЕТ')
        
        self.layoutBox = QVBoxLayout(self)
        self.toolbar = None
        
        if (self.IsToolBar and self.metaInfo.get("isVisibleToolBar", True)):
            self._refreshToolBar()
            self.layoutBox.addWidget(self.toolbar)
        else:
            self.registry.register(self)

        self.spliter = QSplitter(self)
        self.layoutBox.addWidget(self.spliter)

        self.dictChilders = {
            'left': {'form':[], 'group': None},
            'right': {'form':[], 'group': None}
        }
        self.createDictChilders()

        self.createGroupForm('left')
        self.spliter.addWidget(self._createMainFrameWidget())
        self.createGroupForm('right')

    def getForOpen(self):
        return (self, self.caption)

    def createDictChilders(self):
        for chelder in self.getChilders() or []:
            self.dictChilders[chelder.locat]['form'].append(chelder)

    def createGroupForm(self, l: str):
        if self.dictChilders[l]['form'] != []: 
            group = self.dictChilders[l]['group'] = GroupForm(self)
            self.spliter.addWidget(group)
            for form in self.dictChilders[l]['form']:
                f = form.open()
                f.formParent = self
                group.addWidget(f)
                group

    def refreshCh(self):
        for i in self.dictChilders:
            if self.dictChilders[i]['form'] != []:
                self.dictChilders[i]['group'].refreshCh()

    def _set_value_avi(self, attrName:str, setter: SetterEvent):
        setName = f'set{attrName}'
        if hasattr(self, setName):
            getattr(self, setName)(setter)

    def _refreshToolBar(self):
        self.registry.register(self)
        self.toolbar = self.oper.build_toolbar(self.toolbar)

    def _onRefresh(self):...           
    def getChilders(self)->Generator[Any, None, None]:...
    def _getAttr(self, sysName:str): None
    def _onRefresh(self):...
    def onRefresh(self):...
    def _createMainFrameWidget(self)->QWidget: ...
    def _getAttr(self, name)->Optional[Any]: ...
    def checwork(self):...
    