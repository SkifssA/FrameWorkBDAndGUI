from PyQt6.QtWidgets import QCheckBox, QStyle
from PyQt6.QtCore import Qt
from core.ui.inputs.base import Base

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

    def mousePressEvent(self, event):
        """Клик по области ячейки (вне самого индикатора) тоже переключает чекбокс."""
        if event.button() == Qt.MouseButton.LeftButton and self._editor is not None:
            if not self._hitCheckbox(event.position().toPoint()):
                self._editor.click()
                event.accept()
                return
        super().mousePressEvent(event)

    def regSetter(self, fun):
        self.fun = fun

    def setValue(self, value:bool):
        target = bool(value)
        prev = self._editor.isChecked()
        # Блокируем сигналы на время программной установки значения,
        # чтобы не дёргать setter (toggled) лишний раз — уведомим сами ниже.
        self._editor.blockSignals(True)
        self._editor.setChecked(target)
        self._editor.blockSignals(False)
        if prev != target and self.fun:
            self.fun()

    def getValue(self):
        return {
            'value': self._editor.isChecked()
        }