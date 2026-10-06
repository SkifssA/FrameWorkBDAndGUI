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

from engineQT.ui.forms.base import Base
from engineQT.ui.inputs.checkBox import CheckBox
from engineQT.fabric.InputList import InputListConstruct
from engineQT.type.Event import SetterEvent

class List(Base):
    def __init__(self):
        self.systemName = {}
        self.attrHide = []
        self.tablet = None
        super().__init__()
        self.attr = InputListConstruct(self)

    def _createMainFrameWidget(self):
        self._onRefresh()

        self.tablet.itemSelectionChanged.connect(self.refreshCh)
        self.tablet.itemSelectionChanged.connect(self.checwork)
        self.tablet.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self.tablet.cellDoubleClicked.connect(lambda r, c: self.attr.openEditor(r, c))

        return self.tablet

    def _registerHeader(self):
        if self.tablet is None:
            self.head = self._getHeaderLabelsMeta()
            self.tablet = QTableWidget(0, len(self.head))
            self.tablet.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Interactive)
            self.tablet.setHorizontalHeaderLabels(self.head)
            self._reSizeColunm()
            self.tablet.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
            self.tablet.selectRow(0)
            self.tablet.verticalHeader().setVisible(False)

            self.tablet.setShowGrid(False)
            self.tablet.setAlternatingRowColors(True)
            self.tablet.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)

            for i in self.attrHide:
                self.tablet.setColumnHidden(self.systemName[i], True)

    def _getHeaderLabelsMeta(self):
        dataAttrs = self.metaInfo.attr
        res = []
        for i in sorted(list(dict.fromkeys(list(dataAttrs.keys()) + self.Rect.getAttr()))
                        , key=lambda x: self.metaInfo['attr'].get(x, {}).get('order', 10000)):
            dataAttr = dataAttrs.get(i, {})
            res.append(dataAttr.get('caption', i))
            self.systemName[i] = len(res) - 1 
            if not dataAttr.get('isVisible', True):
                self.attrHide.append(i)
        return res

    def _reSizeColunm(self):
        for i in self.systemName.keys():
            if(x:=self.metaInfo['attr'].get(i, {}).get('length')):
                self.tablet.setColumnWidth(self.systemName[i], x)

    def _add_row(self, data):
        currentRow = self.tablet.rowCount()
        self.tablet.insertRow(currentRow)
        
        for sysName in data:
            dataAttr = self.metaInfo['attr'].get(sysName, {})
            
            if dataAttr.get('edit') == 'check':
                checkbox_container = CheckBox(dataAttr)
                checkbox_container.setValue(data[sysName])
                checkbox_container._editor.setEnabled(False)
                self.tablet.setCellWidget(currentRow, self.systemName[sysName], checkbox_container)
            else:
                self.tablet.setItem(currentRow, self.systemName[sysName], QTableWidgetItem(str(data[sysName])))
                
        if (currentRow == 0):
            self.tablet.selectRow(currentRow)

    def _onRefresh(self):
        self.Rect.refresh()
        self._registerHeader()
        self.tablet.setRowCount(0)
        for i in self.Rect.getData():
            self._add_row(i)

    def _getSysNameAttrByCol(self, col: int)->str:
        return list(i for i in self.systemName if self.systemName[i] == col)[0]

    def _getCheckBox(self, row, col)->CheckBox:
        container = self.tablet.cellWidget(row, col)
        if container and container.layout():
            if isinstance(container, CheckBox):
                return container

    def _getAttr(self, sysName: str)->Optional[Any]:
        indRow = self.tablet.currentRow()
        indCollunm = self.systemName[sysName]
        item = self.tablet.item(indRow, indCollunm)
        if item is None:
            item = self.tablet.cellWidget(indRow, indCollunm)
            if isinstance(item, CheckBox):
                return item.getValue()['value']
            return None
        return item.text() if item else None

    def _setAttr(self, sysName: str, value):
        indRow = self.tablet.currentRow()
        indCollunm = self.systemName[sysName]
        item = self.tablet.item(indRow, indCollunm)
        if item is None:
            item = self.tablet.cellWidget(indRow, indCollunm)
            if isinstance(item, CheckBox):
                item.setValue(bool(value))
        else:
            item.setText(str(value))

    def _setUserData(self, sysName: str, value):
        indRow = self.tablet.currentRow()
        indCollunm = self.systemName[sysName]
        if (item:=self.tablet.item(indRow, indCollunm)):
            item.setData(Qt.ItemDataRole.UserRole, value)
    
    def _getUserData(self, sysName: str):
        indRow = self.tablet.currentRow()
        indCollunm = self.systemName[sysName]
        if (item:=self.tablet.item(indRow, indCollunm)):
            return item.data(Qt.ItemDataRole.UserRole)

    def _getAttrMeta(self, sysName)->dict:
        return self.metaInfo['attr'].get(sysName, {})