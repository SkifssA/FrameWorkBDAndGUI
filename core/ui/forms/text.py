from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QLabel, QTableWidget, QTableWidgetItem, 
    QTabWidget, QGroupBox, QLineEdit, QComboBox, QCheckBox,
    QSystemTrayIcon, QMenu, QMessageBox, QSplitter, QFrame, QTextEdit
)
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QHeaderView

from core.ui.forms.base import Base

class Text(Base):
    def _createMainFrameWidget(self):
        self.text = QTextEdit()
        self.text.setReadOnly = True
        return self.text

    def _onRefresh(self):
        self.text.setPlainText(self.onRefresh())
        