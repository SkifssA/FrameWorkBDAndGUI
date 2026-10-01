from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QLabel, QTableWidget, QTableWidgetItem, 
    QTabWidget, QGroupBox, QLineEdit, QComboBox, QCheckBox,
    QSystemTrayIcon, QMenu, QMessageBox, QSplitter, QFrame
)
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QHeaderView

from core.fabric.InputCard import InputCardConstruct
from core.ui.forms.card import Card, BaseForm
from core.package.Rect import Rect

class FilterBar(Card):
    def __init__(self, formParent: BaseForm):
        self.attr = InputCardConstruct(self)
        self.formParent = formParent
        super().__init__()
        self.Rect = Rect(self.formParent)

    def _createMainFrameWidget(self):
        self._widget = QWidget()
        self._layout = QHBoxLayout()
        self._widget.setLayout(self._layout)
        
        self.metaInfo = self.formParent.metaInfo['filter']
        for filter in self.metaInfo:
            for filterAttr in filter['attr'].keys():
                self.attr.createInput(filterAttr, None, filter['attr'][filterAttr])

        return self._widget

    def sizeHint(self):
        return self._old_sizeHint()

    def _getWhere(self):
        return ' and '.join(x for i in self.metaInfo if (x:=i.get('sql')) and '' not in self.Rect._getSqlAndParam(x)[1])
