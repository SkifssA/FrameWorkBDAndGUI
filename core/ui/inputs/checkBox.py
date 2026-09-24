from PyQt6.QtWidgets import QCheckBox
from PyQt6.QtCore import Qt
from core.ui.inputs.base import Base

class CheckBox(Base):
    def createInput(self):
        self._layout.setContentsMargins(0, 0, 0, 0)  # Убираем отступы
        self._layout.setAlignment(Qt.AlignmentFlag.AlignCenter)  # Центрируем
        # Создаем чекбокс
        self._editor = QCheckBox()
        self._editor.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents)

    def regSetter(self, fun):
        self.fun = fun

    def setValue(self, value:bool):
        self._editor.setChecked(bool(value))
        if self.fun:
            self.fun()

    def getValue(self):
        return {
            'value': self._editor.isChecked()
        }