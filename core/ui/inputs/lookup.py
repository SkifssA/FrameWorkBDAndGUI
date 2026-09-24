from PyQt6.QtWidgets import QComboBox
from core.package.ActionDispatcher import ActionDispatcherPkg
from core.ui.inputs.base import Base

class LookUp(Base):
    def createInput(self):
        self.loadDataLookUp = ActionDispatcherPkg().action(f"{self.dataAttr['refTab']}Avi.{self.dataAttr['display']}", kattr={}).getData()
        self._editor = QComboBox()
        for dataLook in self.loadDataLookUp:
            self._editor.addItem(dataLook['sHeadLine'], dataLook['id'])

        self._editor.setFrame(False)
        self._editor.setStyleSheet("""
            QComboBox { 
                background: black; 
                padding: 2px; 
                border: 1px solid #aaa; 
            }
        """)

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
        self._editor.currentIndexChanged.connect(fun)
        
        # Переопределяем focusOutEvent через установку атрибута
        original_focus_out = self._editor.focusOutEvent
        def custom_focus_out(event):
            fun()
            original_focus_out(event)
        self.focusOutEvent = custom_focus_out