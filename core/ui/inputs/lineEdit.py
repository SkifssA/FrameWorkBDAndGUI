from PyQt6.QtWidgets import QLineEdit
from core.ui.inputs.base import Base

class LineEdit(Base):        
    def createInput(self):
        self._editor = QLineEdit()
        self._editor.setFrame(False)

    def regSetter(self, fun):
        self.fun = fun
        # Сохранение по Enter или потере фокуса
        self._editor.returnPressed.connect(fun)
        self.focusOutEvent = fun

    def setValue(self, value:str):
        if value:
            self._editor.setText(str(value))

    def getValue(self):
        return {
            'value': self._editor.text()
        }