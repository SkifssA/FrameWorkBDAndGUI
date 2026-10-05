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

from engineQT.ui.forms.base import Base as BaseForm
from engineQT.ui.inputs import Base as BaseInput, inputType
from engineQT.ui.widget.inputandlable import InputandLable 
from engineQT.type.Event import SetterEvent
from engineQT.fabric.InputCard import InputCardConstruct

class Card(BaseForm):
    def __init__(self, **kwargs):
        self.obj = None
        self.attr = InputCardConstruct(self)
        super().__init__(**kwargs)

    def _createMainFrameWidget(self):
        self._widget = QWidget()
        self._layout = QVBoxLayout()
        self._widget.setLayout(self._layout)

        self.Rect.refresh()
        self.obj = self.Rect.refreshRes
        values = self.Rect.getData()[0]
        attr = self.Rect.getAttr()

        for name in attr:
            if (not name in ('sHeadLine', 'sMnemoCode')):
                self.attr.createInput(name, values[name])

        self._layout.addStretch()

        return self._widget

    def _onRefresh(self):
        self.Rect.refresh()
        self.obj = self.Rect.refreshRes
        values = self.Rect.getData()[0]
        for item in self.attr.getNameAllEditor():
            self._setAttr(item, values[item])

    def _getAttr(self, name):
        if self.attr._editors.get(name):
            return self.attr._editors[name].getValue()['value']
        if (self.Rect.getData() != []):
            return self.Rect.getData()[0].get(name)
        return None

    def _setAttr(self, name, value):
        self.attr._editors[name].setValue(value)

    def _getAttrMeta(self, sysName)->dict:
        return self.attr.getEditor(sysName).metaInfo