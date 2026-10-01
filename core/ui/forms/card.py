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
from core.ui.inputs import Base as BaseInput, inputType
from core.ui.widget.inputandlable import InputandLable 
from core.type.Event import SetterEvent
from core.fabric.InputCard import InputCardConstruct

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

    def _set_value_avi(self, attrName: str, setter: SetterEvent) -> None:
        """Вызывает сеттер атрибута `set<attrName>`, если он определён."""
        if x:=self.attr.getEditor(attrName).metaInfo.get('attrId'):
            self._setAttr(x, setter.value)
        setName = f'set{attrName}'
        if hasattr(self, setName):
            getattr(self, setName)(setter)