from PyQt6.QtWidgets import QLineEdit
from core.ui.inputs.base import Base

class LineEdit(Base):        
    def createInput(self):
        self._editor = QLineEdit()
        self._editor.setFrame(False)

    def regSetter(self, fun):
        self.fun = fun
        self._editor.returnPressed.connect(lambda *a: fun())
        self._editor.editingFinished.connect(lambda *a: fun())

    def setValue(self, value:str):
        if value:
            self._editor.setText(str(value))

    def getValue(self):
        return {
            'value': self._editor.text()
            , 'user_data': None
        }

    def active(self, value, rect, viewport):
        super().active(value, rect, viewport)
        from core.ui.theme import C
        self.setStyleSheet(
            f"background: {C.CARD}; border: 1px solid {C.ACCENT}; border-radius: 6px; padding: 2px;"
        )
        
        self.show()
        self._editor.selectAll()