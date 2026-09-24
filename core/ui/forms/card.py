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

from core.ui.forms.base import Base as BaseForm
from core.ui.inputs import Base as BaseInput, CheckBox, LineEdit, LookUp
from core.ui.widget.inputandlable import InputandLable 
from core.type.Event import SetterEvent

class Card(BaseForm):

    attr = {
        'edit': LineEdit,
        'check': CheckBox,
        'lookUp': LookUp
    }

    def __init__(self, **kwargs):
        self.obj = None
        super().__init__(**kwargs)

    def _createMainFrameWidget(self):
        self._widget = QWidget()
        self._layout = QVBoxLayout()
        self._widget.setLayout(self._layout)
        self._editors: dict[str, BaseInput] = {}
        self._InputandLable:dict[str, InputandLable] = {}

        self.Rect.refresh()
        self.obj = self.Rect.refreshRes
        values = self.Rect.getData()[0]
        attr = self.Rect.getAttr()

        for name in attr:
            self._addInput(name)
            self._editors[name].setValue(values[name]) 

        self._layout.addStretch()

        return self._widget

    def _onRefresh(self):
        self.Rect.refresh()
        self.obj = self.Rect.refreshRes
        values = self.Rect.getData()[0]
        for item, value in self._editors.items():
            value.setValue(values[item])

    def _addInput(self, name):
        data = self.metaInfo['attr'].get(name, {})
        self._editors[name] = self.attr[data.get('edit', 'edit')](data)
        self._InputandLable[name] = InputandLable(data.get('caption', name), self._editors[name]) 
        self._layout.addWidget(self._InputandLable[name])
        self._InputandLable[name].setVisible(data.get('isVisible', True))
        self._editors[name].regSetter(
            lambda: self._set_value_avi(name, SetterEvent(self._editors[name]))
        )

    def _getAttr(self, name):
        if self.obj and hasattr(self.obj, name):
            return self.obj.__dict__[name]
        elif self._editors.get(name):
            return self._editors[name].getValue()['value']
        else:
            return self.Rect.getData()[0][name]