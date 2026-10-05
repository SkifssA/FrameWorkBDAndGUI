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

class InputandLable(QWidget):
    def __init__(self, lable: str, input: QWidget):
        super().__init__()
        self.setObjectName("FieldRow")  # подпись красится темой (GLOBAL_QSS)
        self.la = QHBoxLayout()
        self.setLayout(self.la)

        self.la.addWidget(QLabel(lable))
        self.la.addWidget(input)