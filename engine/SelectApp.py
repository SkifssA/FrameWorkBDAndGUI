from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QLabel, QTableWidget, QTableWidgetItem, 
    QTabWidget, QGroupBox, QLineEdit, QComboBox, QCheckBox,
    QSystemTrayIcon, QMenu, QMessageBox, QSplitter, QFrame
)
from PyQt6.QtCore import Qt

from engine.package import FileManagerPkg, ActionDispatcher, asyncRun

class SelectApp:
    def open(self, parent:QMainWindow):
        container = QWidget()
        layout = QVBoxLayout()
        container.setLayout(layout)

        listApp = asyncRun(FileManagerPkg.ReadFile("../project.yaml"))
        for app in listApp['modules']:
            if asyncRun(FileManagerPkg.Exists(f"../modules/{app}/config/app.json")):
                data = asyncRun(FileManagerPkg.ReadFile(f"../modules/{app}/config/app.json"))
                if (data.get('name', None) is not None):
                    self.createBlocApp(data, layout)

        layout.addStretch()
        parent.setCentralWidget(container)

    def createBlocApp(self, data, layout:QVBoxLayout):
        w = QWidget()
        layoutW = QHBoxLayout()

        label = QLabel(data['name'])
        button = QPushButton('Открыть')

        layoutW.addWidget(label)
        layoutW.addWidget(button)
        button.clicked.connect(lambda: self.openMainMenuModule(data))

        w.setLayout(layoutW)
        layout.addWidget(w)

    def openMainMenuModule(self, data):
        module_name = f"Awh_AnimeAvi.DviDefault"
        ActionDispatcher().action(module_name).open()

        