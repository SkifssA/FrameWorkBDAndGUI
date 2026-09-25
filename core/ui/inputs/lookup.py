from PyQt6.QtWidgets import QComboBox
from core.package.ActionDispatcher import ActionDispatcherPkg
from core.ui.inputs.base import Base

class LookUp(Base):
    def createInput(self):
        self.loadDataLookUp = ActionDispatcherPkg().action(f"{self.dataAttr['refTab']}Avi.{self.dataAttr['display']}", kattr={}).getData()
        self._editor = QComboBox()
        for dataLook in self.loadDataLookUp:
            self._editor.addItem(dataLook['sHeadLine'], dataLook['id'])


    def setValue(self, value):
        self._editor.setCurrentText(str(value))

    def getValue(self):
        index = self._editor.currentIndex()
        return {
            'data': self._editor.itemData(index)
            ,'value': self._editor.itemText(index)
        }

    def regSetter(self, fun):
        self.fun = fun
        self._editor.currentIndexChanged.connect(lambda *a: fun())