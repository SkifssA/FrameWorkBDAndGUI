import sys
import asyncio
import inspect
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QLabel, QTableWidget, QTableWidgetItem, 
    QTabWidget, QGroupBox, QLineEdit, QComboBox, QCheckBox,
    QSystemTrayIcon, QMenu, QMessageBox, QSplitter, QFrame, 
    QMenuBar, QToolBar
)
from PyQt6.QtGui import QIcon, QKeySequence, QAction
from PyQt6.QtCore import Qt

from core.fabric.Oper import OperRegistry
from core.package.FileManager import FileManagerPkg

# --- 3. Билдер (Исправленная логика) ---
class OperUIBuilder:
    def __init__(self, registry: OperRegistry):
        self.registry = registry
        self.oper:dict[str, QAction] = {}

    def build_menubar(self, window: QMainWindow) -> QMenuBar:
        menubar = window.menuBar()
        # Получаем ТОЛЬКО корневые операции (у которых нет родителя)
        root_ops = self.registry.get_children(parent_id=None)
        
        for op in root_ops:
            self._add_to_menu(menubar, op)
            
        return menubar

    def isVisible(self, nameOpers: list, value: bool):
        if (value is not None):
            for i in nameOpers:
                if (x:=self.oper.get(i)) is not None:
                    x.setVisible(value)

    def isEnabled(self, nameOpers: list, value: bool):
        if (value is not None):
            for i in nameOpers:
                if (x:=self.oper.get(i)) is not None:
                    x.setEnabled(value)
    
    def build_toolbar(self, toolBar:QToolBar=None) -> QToolBar:
        if toolBar:
            toolbar = toolBar
            toolbar.clear()
        else:
            toolbar = QToolBar("Основная панель")

        toolbar.setFloatable(False)
        toolbar.setMovable(False)

        root_ops = self.registry.get_children()

        for op in root_ops:
            self._add_action(toolbar, op)

        return toolbar

    def _add_action(self, parent_widget, op: dict):
        action = QAction(op['label'], parent_widget)
                                
        if op.get('icon'):
            realPath = FileManagerPkg.getRealPath("core/assets/img/icon/" + op['icon'])
            action.setIcon(QIcon(realPath))
        if op.get('shortcut'):
            action.setShortcut(QKeySequence(op['shortcut']))
        if op.get('tooltip'):
            action.setToolTip(op['tooltip'])
            
        action.setCheckable(op.get('checkable', False))
        
        # Обертка для async/sync
        handler = op['handler']
        def make_callback(h):
            def wrapper():
                QApplication.setOverrideCursor(Qt.CursorShape.WaitCursor)
                res = h()
                if inspect.iscoroutine(res):
                    asyncio.ensure_future(res)
                QApplication.restoreOverrideCursor()
            return wrapper
        
        action.triggered.connect(make_callback(handler))
        self.oper[op['id']] = action
        parent_widget.addAction(action)

    def _add_to_menu(self, parent_widget, op: dict):
        """
        parent_widget может быть QMenuBar (для корня) или QMenu (для подменю)
        """
        children = self.registry.get_children(op['id'])
        has_children = len(children) > 0

        # Сценарий А: Это папка (есть дети) -> Создаем QMenu
        if has_children:
            submenu = parent_widget.addMenu(op['label'])
            
            # Рекурсивно добавляем детей
            for child_op in children:
                self._add_to_menu(submenu, child_op)
                
        # Сценарий Б: Это лист (нет детей) -> Создаем QAction
        else:
            self._add_action(parent_widget, op)