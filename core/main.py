import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QLabel, QTableWidget, QTableWidgetItem, 
    QTabWidget, QGroupBox, QLineEdit, QComboBox, QCheckBox,
    QSystemTrayIcon, QMenu, QMessageBox, QSplitter, QFrame
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QIcon, QAction

from core.ui.forms.selectApp import SelectApp
from core.package.FileManager import FileManagerPkg
from core.package.ActionDispatcher import ActionDispatcherPkg
from core.ui.theme import apply_theme

class MainWindow(QMainWindow):
    name = "NecoTab"
    pathIco = FileManagerPkg.getRealPath("../assets/img/iconApp/app.ico")

    def __init__(self):
        super().__init__()
        self.ico = QIcon(self.pathIco)
        self.setWindowTitle(self.name)
        self.setGeometry(100, 100, 1200, 800)
        self.setWindowIcon(self.ico)
        self.createSystemTray()
        self.setCentralWidget(SelectApp())
        ActionDispatcherPkg().action("Bc_ScriptSchedulerPkg.run", classMethod=True)
        
    def createSystemTray(self):
        # Создаем системный трей
        self.tray_icon = QSystemTrayIcon(self)
        self.tray_icon.setIcon(self.ico)
        self.tray_icon.setToolTip(self.name)
        
        # Создаем меню для трея
        tray_menu = QMenu()
        
        action_show = QAction("Показать", self)
        action_show.triggered.connect(self.show)
        
        action_hide = QAction("Скрыть", self)
        action_hide.triggered.connect(self.hide)
        
        action_quit = QAction("Выход", self)
        action_quit.triggered.connect(QApplication.quit)
        
        tray_menu.addAction(action_show)
        tray_menu.addAction(action_hide)
        tray_menu.addSeparator()
        tray_menu.addAction(action_quit)
        
        self.tray_icon.setContextMenu(tray_menu)
        self.tray_icon.show()
        
        # Обработка клика по иконке в трее
        self.tray_icon.activated.connect(self.on_tray_activated)
    
    def on_tray_activated(self, reason):
        if reason == QSystemTrayIcon.ActivationReason.Trigger:
            # Двойной клик или одинарный (зависит от ОС)
            if self.isVisible():
                self.hide()
            else:
                self.show()

    def returnMainScreen(self):
        self.setMenuBar(None)
        self.setCentralWidget(SelectApp())
    
    def closeEvent(self, event):
        # При закрытии сворачиваем в трей вместо выхода
        event.ignore()
        self.hide()
        self.returnMainScreen()
        # self.tray_icon.showMessage(
        #     "Приложение свернуто",
        #     "Приложение работает в фоновом режиме",
        #     QSystemTrayIcon.MessageIcon.Information,
        #     2000
        # )

def mainProgram():
    app = QApplication(sys.argv)
    apply_theme(app)

    if not QSystemTrayIcon.isSystemTrayAvailable():
        print("Системный трей не поддерживается")
        sys.exit(1)

    window = MainWindow()
    window.show()

    sys.exit(app.exec())

async def w():
    from module.awh.object.Awh_AnimeLoadPkg import Awh_AnimeLoadPkg
    from module.awh.object.anime.Awh_AnimeApi import Awh_AnimeApi
    
    url = 'https://animego.me/anime/ya-perevoplotilsya-v-goblina-voprosy-yest-4007'
    obj = await Awh_AnimeLoadPkg().init()
    data = await obj.getData(url)
    Awh_AnimeApi().register(data)

if __name__ == '__main__':
    # mainProgram()

    from core.package.AsynRun import asyncRun
    asyncRun(w())