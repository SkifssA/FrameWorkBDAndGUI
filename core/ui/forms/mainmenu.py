from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QLabel, QTableWidget, QTableWidgetItem, 
    QTabWidget, QGroupBox, QLineEdit, QComboBox, QCheckBox,
    QSystemTrayIcon, QMenu, QMessageBox, QSplitter, QFrame
)
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QHeaderView
from PyQt6.QtGui import QAction, QKeySequence

from core.ui.forms.base import Base
from core.ui.widget.menubar import SetOper

class MainMenu(Base):

    IsToolBar = False

    def __init__(self, mainWin:QMainWindow):
        self.mainWin = mainWin
        super().__init__()

    def _createMainFrameWidget(self):

        self.mainWin.setMenuBar(self.oper.build_menubar(self.mainWin))

        self.tab_widget = QTabWidget()
        return self.tab_widget

    @SetOper(label="Приложение", order=0)
    def menu_file(self): pass

    @SetOper(label="Выход", headOper="menu_file", order=100, shortcut="Ctrl+Q", icon="icons/exit.png")
    def exit_app(self):
        from core.ui.forms.selectApp import SelectApp
        self.mainWin.returnMainScreen()

    def close_tab_by_title(self, title):
        """Закрыть вкладку по её заголовку"""
        for i in range(self.tab_widget.count()):
            if self.tab_widget.tabText(i) == title:
                self.tab_widget.removeTab(i)
                return True
        return False