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

from core.package.FileManager import FileManagerPkg

# --- 1. Декоратор ---
def SetOper(label: str = None, order: int = 0, headOper: str = None, 
            isVisible: bool = True, icon: str = None, shortcut: str = None, 
            isCheckable: bool = False, tooltip: str = None):
    def decorator(func):
        func._is_oper_handler = True
        func._oper_id = func.__name__
        func._oper_label = label or func._oper_id.replace('_', ' ').title()
        func._order = order
        func._headOper = headOper
        func._isVisible = isVisible
        func._icon_path = icon
        func._shortcut = shortcut
        func._isCheckable = isCheckable
        func._tooltip = tooltip
        return func
    return decorator

# --- 2. Реестр ---
class OperRegistry:
    def __init__(self):
        self._flat_ops = []

    def register(self, instance):
        self._flat_ops = []
        for name, method in inspect.getmembers(instance, predicate=inspect.ismethod):
            if getattr(method, '_is_oper_handler', False):
                self._flat_ops.append({
                    'id': method._oper_id,
                    'label': method._oper_label,
                    'order': method._order,
                    'headOper': method._headOper,
                    'isVisible': method._isVisible,
                    'icon': method._icon_path,
                    'shortcut': method._shortcut,
                    'checkable': method._isCheckable,
                    'tooltip': method._tooltip,
                    'handler': method
                })
        self._flat_ops.sort(key=lambda x: x['order'])

    def get_children(self, parent_id=None):
        # Для корневых элементов headOper должен быть None
        return [op for op in self._flat_ops 
                if op['isVisible'] and op['headOper'] == parent_id]

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
                            x.setEnabled

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
                res = h()
                if inspect.iscoroutine(res):
                    asyncio.ensure_future(res)
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