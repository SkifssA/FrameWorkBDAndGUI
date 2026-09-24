from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QLabel, QTableWidget, QTableWidgetItem, 
    QTabWidget, QGroupBox, QLineEdit, QComboBox, QCheckBox,
    QSystemTrayIcon, QMenu, QMessageBox, QSplitter, QFrame,
    QSizePolicy
)
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QHeaderView, QAbstractItemView
from typing import Optional, Any

class Base(QWidget):
    def __init__(self, dataAttr:dict):
        super().__init__()
        self.dataAttr = dataAttr
        self._layout = QHBoxLayout()
        self.setLayout(self._layout)
        self._layout.setContentsMargins(0, 0, 0, 0)  # <-- Убираем отступы
        self._layout.setSpacing(0)  # <-- Убираем промежутки между виджетами
        self.fun = None
        
        self._editor:QWidget = None
        
        self.createInput()
        self._layout.addWidget(self._editor)

    def createInput(self)->QWidget:...
    def getValue(self)->dict[str, Any]:...
    def setValue(self, value):...
    def regSetter(self, fun):...