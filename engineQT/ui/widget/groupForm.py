from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QLabel, QTableWidget, QTableWidgetItem, 
    QTabWidget, QGroupBox, QLineEdit, QComboBox, QCheckBox,
    QSystemTrayIcon, QMenu, QMessageBox, QSplitter, QFrame
)
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QHeaderView

class GroupForm(QWidget):
    def __init__(self, parent: QWidget):
        super().__init__(parent)
        self.layoutBox = QVBoxLayout()
        self.spliter = QSplitter(self)
        self.spliter.setOrientation(Qt.Orientation.Vertical)
        self.layoutBox.addWidget(self.spliter)
        self.setLayout(self.layoutBox)
        self.lWidCh = []

    def addWidget(self, widget):
        self.spliter.addWidget(widget)
        widget._onRefresh()
        self.lWidCh.append(widget)

    def refreshCh(self):
        for i in self.lWidCh:
            i._onRefresh()