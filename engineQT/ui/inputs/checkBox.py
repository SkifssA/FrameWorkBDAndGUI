from PyQt6.QtWidgets import QCheckBox, QStyle
from PyQt6.QtCore import Qt
from engineQT.ui.inputs.base import Base

class CheckBox(Base):
    def createInput(self):
        self._layout.setContentsMargins(0, 0, 0, 0)  # Убираем отступы
        self._layout.setAlignment(Qt.AlignmentFlag.AlignCenter)  # Центрируем
        # Создаем чекбокс
        self._editor = QCheckBox()
        self._editor.toggled.connect(self._onToggled)

    def _onToggled(self, _checked: bool):
        if self.fun:
            self.fun()

    def _hitCheckbox(self, pos) -> bool:
        """Попадание в чекбокс: геометрия + хит-тест стиля (с учётом QSS-индикатора)."""
        chk = self._editor
        if not chk.geometry().contains(pos):
            return False
        try:
            from PyQt6.QtWidgets import QStyleOptionButton
            opt = QStyleOptionButton()
            chk.initStyleOption(opt)
            # координаты pos — от контейнера; переводим в координаты чекбокса
            local = pos - chk.geometry().topLeft()
            sub, _ = chk.style().complexControl(opt, chk.rect())
            if sub is not None and sub.subControl in (
                    QStyle.SubControl.SC_CheckIndicator, QStyle.SubControl.SC_Indicator):
                r = sub.subControlRect(chk.style(), opt, sub.subControl, chk.rect())
                return r.adjusted(-4, -4, 4, 4).contains(local)
        except Exception:
            pass
        return True

    def regSetter(self, fun):
        self._editor.toggled.connect(fun)

    def setValue(self, value:bool):
        target = bool(value)
        prev = self._editor.isChecked()
        self._editor.setChecked(target)
        if prev != target and self.fun:
            self.fun()

    def getValue(self):
        return {
            'value': self._editor.isChecked()
            , 'user_data': None
        }

    def active(self, value, viewport):
        self.setValue(not value)