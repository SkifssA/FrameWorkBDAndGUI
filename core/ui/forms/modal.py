from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QTableWidget, QTableWidgetItem, QDialog, 
    QLineEdit, QLabel, QMessageBox
)
from PyQt6.QtCore import Qt
import types

from core.ui.forms.base import Base
from core.ui.widget.menubar import SetOper

class Modal(QDialog):
    def __init__(self, cls:type[Base], result:list[str]):
        super().__init__()
        self._layout = QVBoxLayout()
        self._form = cls()
        self._result = result
        self._addOperOkClose()
        self.setWindowTitle(self._form.caption)
        self._layout.addWidget(self._form)
        self.setLayout(self._layout)

    def getResult(self):
        res = {}
        for i in self._result:
            res[i] = self._form._getAttr(i)
        return res

    def isAccept(self)->bool:
        return self.exec() == QDialog.DialogCode.Accepted

    def _addOperOkClose(self):
        def OkClose(selfForm):
            self.accept()

        fun = SetOper(label='Выбрать', order=-1000, icon='selected.png')(OkClose)
        self._form.OkClose = types.MethodType(fun, self._form)

        self._form._refreshToolBar()