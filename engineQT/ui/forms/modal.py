from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QTableWidget, QTableWidgetItem, QDialog, 
    QLineEdit, QLabel, QMessageBox
)
from PyQt6.QtCore import Qt, QSize
from PyQt6.QtGui import QIcon
import types

from engineQT.ui.forms.base import Base
from core.fabric.Oper import SetOper
from core.package.FileManager import FileManagerPkg
from core import PATHICO

class Modal(QDialog):
    def __init__(self, cls:type[Base], result:list[str]):
        super().__init__()
        self._layout = QVBoxLayout()
        self._form = cls()
        self._form.formParent = self
        self._result = result
        self._addOperOkClose()
        self.setWindowTitle(self._form.caption)
        self._layout.addWidget(self._form)
        self.setLayout(self._layout)
        self.resize(QSize(
            self._form.metaInfo.get('width', self._form.width())
            , self._form.metaInfo.get('height', self._form.height())
        ))

        self.ico = QIcon(PATHICO)
        self.setWindowIcon(self.ico)

    def getResult(self):
        res = {}
        for i in self._result:
            res[i] = self._form._getAttr(i)
        return res

    def close(self, _):
        super().close()

    def isAccept(self)->bool:
        return self.exec() == QDialog.DialogCode.Accepted

    def _addOperOkClose(self):
        def OkClose(selfForm):
            self.accept()
            QApplication.setOverrideCursor(Qt.CursorShape.WaitCursor)

        fun = SetOper(label='Выбрать', order=-1000, icon='selected.png')(OkClose)
        self._form.OkClose = types.MethodType(fun, self._form)

        self._form._refreshToolBar()