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

from engine.SelectApp import SelectApp

def mainProgram():
    app = QApplication(sys.argv)
        
    # Установка стиля приложения
    app.setStyle("Fusion")
    
    window = QMainWindow()
    window.setWindowTitle("NecoTab")
    window.setGeometry(100, 100, 1200, 800)

    SelectApp().open(window)

    window.show()
    
    sys.exit(app.exec())

if __name__ == '__main__':
    mainProgram()