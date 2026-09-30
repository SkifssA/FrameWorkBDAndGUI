from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QLabel, QTableWidget, QTableWidgetItem, 
    QTabWidget, QGroupBox, QLineEdit, QComboBox, QCheckBox,
    QSystemTrayIcon, QMenu, QMessageBox, QSplitter, QFrame,
    QSizePolicy
)
from PyQt6.QtCore import Qt, QEvent
from PyQt6.QtWidgets import QHeaderView, QAbstractItemView
from typing import Optional, Any

class Base(QWidget):
    def __init__(self, dataAttr:dict):
        super().__init__()
        self.dataAttr = dataAttr
        self._layout = QHBoxLayout()
        self.setLayout(self._layout)
        self._layout.setContentsMargins(0, 0, 0, 0)
        self._layout.setSpacing(0)
        self.fun = None
        self.typeForm = None

        self.setFocusPolicy(Qt.FocusPolicy.StrongFocus)
        
        self._editor:QWidget = None
        
        self.createInput()
        self._layout.addWidget(self._editor)
        self._editor.installEventFilter(self)

    def focusInEvent(self, event):
        """Переадресуем фокус контейнера на внутреннее поле ввода."""
        if self._editor is not None:
            self._editor.setFocus()
        super().focusInEvent(event)

    def active(self, value, viewport):
        self.setValue(value)
        self.setParent(viewport)

    def setTypeForm(self, typeForm):
        self.typeForm = typeForm

    def regSetter(self, fun):...
    def createInput(self)->QWidget:...
    def getValue(self)->dict[str, Any]:...
    def setValue(self, value):...