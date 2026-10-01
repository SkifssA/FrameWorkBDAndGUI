from PyQt6.QtWidgets import QComboBox
from core import ACTIONDISPATCHER
from core.ui.inputs.base import Base

class LookUp(Base):
    def createInput(self):
        self.loadDataLookUp = ACTIONDISPATCHER.action(f"{self.metaInfo['refTab']}Avi.{self.metaInfo['display']}", kattr={}).getData()
        self._editor = QComboBox()
        for dataLook in self.loadDataLookUp:
            self._editor.addItem(dataLook['sHeadLine'], dataLook['id'])
        self._editor.setCurrentIndex(-1)

    def regSetter(self, fun):
        self.fun = fun
        self._editor.currentIndexChanged.connect(lambda *a: fun())

    def setValue(self, value):
        self._editor.setCurrentText(str(value))

    def getValue(self):
        index = self._editor.currentIndex()
        return {
            'user_data': self._editor.itemText(index)
            , 'value': self._editor.itemData(index)
        }

    def active(self, value, viewport):
        super().active(value, viewport)
        self._editor.showPopup()